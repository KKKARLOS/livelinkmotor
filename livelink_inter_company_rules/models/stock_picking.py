# -*- coding: utf-8 -*-
from shutil import move
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    has_virtual_serials = fields.Integer('Virtuals',
            compute='_compute_virtuals')
    is_intercompany = fields.Boolean('Is intercompany?',
            compute='_compute_intercompany')

    def _compute_virtuals(self):
        diff = 0
        for move in self.move_ids_without_package:
            aux = move.product_uom_qty - move.quantity_done
            if aux and move.count_virtual_serials != 0 \
                     and move.count_virtual_serials > move.quantity_done:
                diff += 1
        self.has_virtual_serials = diff

    def _compute_intercompany(self):
        recSO = self.env['sale.order']
        if self.purchase_id:
            cids = self.env['res.company'].sudo().search([]).ids
            recSO = recSO.with_context(allowed_company_ids=cids)
            args = [
                ('auto_purchase_order_id', '=', self.purchase_id.id),
                ('state', 'in', ['sale', 'done'])
            ]
            recSO |= recSO.search(args, limit=1)
        self.is_intercompany = bool(recSO)

    def action_cancel(self):
        res = super(StockPicking, self).action_cancel()
        self.mapped('move_ids_without_package.intercompany_serial_ids').unlink()
        return res

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        if self.is_intercompany:
            cids = self.env['res.company'].sudo().search([]).ids
            sself = self.with_context(allowed_company_ids=cids)
            for op in sself.move_ids_without_package: op.validate_ext_operations()
        return res

    def action_fill_suggesteds(self):
        self.action_assign()
        for op in self.move_ids_without_package: op.action_fill_suggesteds()

    def action_update_suggesteds_from_main_company(self, move, product_id, lots):
        move_lines = self.move_line_ids_without_package.filtered(lambda r:
                        r.product_id == product_id)
        union = lots & move_lines.mapped('lot_id')
        if union:
            lots -= union
            move_lines = move_lines.filtered(lambda r: r.lot_id not in union)
        qtyL = len(move_lines)
        qtyN = len(lots)
        qty = qtyL if qtyL <= qtyN else qtyN
        lines = False
        if qtyL > qtyN:
            lines = move_lines[:qtyN]
            move_lines[qtyN:].unlink()
        else: lines = move_lines
        if qtyL < qtyN: self._generate_new_lines_by_lots(move, lots[qtyL:])
        [lines[r].write({'lot_id': lots[r].id}) for r in range(qty)]

    def _generate_new_lines_by_lots(self, move, lots):
        new_lines = [(0, 0, self._prepare_new_move_line(move, lot)) for lot in lots]        
        self.write({'move_line_ids_without_package': new_lines})

    def _prepare_new_move_line(self, move, lot):
        return {
            'lot_id': lot.id,
            'product_uom_id': lot.product_id.uom_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'product_uom_qty': 1,
            'product_id': lot.product_id.id,
            'move_id': move.id,
            'state': 'assigned',
        }
            
