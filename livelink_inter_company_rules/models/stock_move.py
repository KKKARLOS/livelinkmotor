# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class StockMove(models.Model):
    _inherit = 'stock.move'

    intercompany_serial_ids = fields.One2many('stock.production.virtual.lot',
            'intercompany_move_id', string="Custom Values")
    count_virtual_serials = fields.Integer('Virtuals',
            compute='_compute_virtuals')

    def _compute_virtuals(self):
        for move in self:
            virtuals = move.intercompany_serial_ids
            valids = virtuals.filtered(lambda r: r.state=='confirmed')
            move.count_virtual_serials = len(valids)

    def action_view_validate_serials(self):
        module = 'livelink_inter_company_rules'
        action_name = 'action_serial_intercompany_moves'
        action = self.env.ref('%s.%s' % (module, action_name)).read()[0]
        action['domain'] = [('id', 'in', self.intercompany_serial_ids.ids)]
        context = {
            'default_intercompany_move_id': self.id,
            'default_intercompany_picking_id': self.picking_id.id,
            'default_product_id': self.product_id.id,
        }
        action['context'] = context
        return action

    def validate_ext_operations(self):
        objPick = self.env['stock.picking']
        for move in self:
            names = move.mapped('move_line_nosuggest_ids.lot_name')
            recSO = move._get_ext_sale_order()
            if recSO and names:
                domain = [
                    ('product_id', '=', move.product_id.id),
                    ('state', '=', 'confirmed'),
                    ('name', 'in', names),
                ]
                virtual_lots = move._get_virtual_lots(domain)
                recLots = virtual_lots.mapped('intercompany_ext_lot_id')
                if recLots:
                    args = [
                        ('state', 'in', ['draft', 'confirmed', 'assigned']),
                        ('sale_id', '=', recSO.id)
                    ]
                    pick = objPick.search(args, limit=1)
                    if pick:
                        pick.action_assign()
                        prod = move.product_id
                        pick.action_update_suggesteds_from_main_company(move, prod, recLots)
                    domain += [('intercompany_move_line_id', '!=', False)]
                    move._get_virtual_lots(domain).write({'state': 'created'})
                    domain = [('intercompany_move_line_id', '=', False)]
                    move._get_virtual_lots(domain).unlink()

    def action_fill_suggesteds(self):
        for move in self: move.action_load_suggesteds()

    def action_load_suggesteds(self):
        self.ensure_one()
        recVirtuals = self._get_virtual_lots([('state', '=', 'confirmed')])
        pending = int(self.product_uom_qty - self.quantity_done)
        qty = pending if pending <= len(recVirtuals) else len(recVirtuals)
        
        lines = self.move_line_ids.filtered(lambda r:
                    r.state == 'assigned' and r.qty_done == 0)
        if len(lines) < qty: qty = len(lines)
        for r in range(qty):
            lines[r].write({
                'qty_done': 1,
                'product_uom_qty': 0,
                'lot_name': recVirtuals[r].name
            })
            recVirtuals[r].write({
                'intercompany_move_line_id': lines[r].id
            })

    def _get_virtual_lots(self, domain=False):
        self.ensure_one()
        args = list(domain) if domain else []
        args += [('intercompany_move_id', '=', self.id)]
        return self.env['stock.production.virtual.lot'].search(args)

    def _get_ext_sale_order(self):
        recSO = self.env['sale.order']
        if self.purchase_line_id.order_id:
            po = self.purchase_line_id.order_id.id
            args = [
                ('auto_purchase_order_id', '=', po),
                ('state', 'in', ['sale', 'done'])
            ]
            return recSO.search(args, limit=1)
        return recSO
