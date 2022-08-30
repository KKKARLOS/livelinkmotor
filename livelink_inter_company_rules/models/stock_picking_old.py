# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import Warning
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_picking import Picking

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()     
        recPicking = self.env['stock.picking']
        for pick in self:
            if pick.company_id.auto_propagate_serials \
                    and pick.picking_type_code == 'outgoing' \
                    and pick.sale_id.auto_purchase_order_id:
                        # 2- Buscar el Pedido de Compra que generó la venta
                rel_purchase_id = pick.sale_id.auto_purchase_order_id
                self._validate_check_access_rights(rel_purchase_id.company_id)
                # Por cada Movimiento 
                for move in pick.move_lines:
                    # 1- if el producto tiene trazabilidad de número serie
                    if move.product_id.tracking == 'serial':
                        recPicking |= move._get_pending_picking(rel_purchase_id)
        # if recPicking:
        #     removes = recPicking.move_line_ids.filtered(lambda l: not l.lot_id)
        #     removes.unlink()
        #     virtuals = [(4, p.id) for p in recPicking]
        #     wiz = self.env['stock.immediate.transfer'].create({'pick_ids': virtuals})
        #     wiz.process()
        return res

    def _validate_check_access_rights(self, company):
        _ic_uid = company.intercompany_user_id \
                    and company.intercompany_user_id.id \
                    or self.env.user.id
        READ_MODELS = ['stock.picking', 'stock.move', 'stock.move.line',
                        'stock.production.lot', 'product.product']
        CREATE_MODELS = ['stock.move.line', 'stock.production.lot']
        for model in READ_MODELS:
            # check intercompany user access rights
            if not self.env[model].with_user(_ic_uid).check_access_rights('read', raise_exception=False):
                raise Warning(_("Inter company user of company %s doesn't have enough access rights") % company.name)
        
        for model in CREATE_MODELS:
            # check intercompany user access rights
            if not self.env[model].with_user(_ic_uid).check_access_rights('create', raise_exception=False):
                raise Warning(_("Inter company user of company %s doesn't have enough access rights") % company.name)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_pending_picking(self, recPO):
        recPicking = self.env['stock.picking']
                        # 3- Buscar los albaranes con estado borrador o en espera
                        # - Buscar los Movimientos con el mismo producto asociado 
                        # y que pertenezcan a los Albaranes anteriores con cantidad > 0
        args = [('state', 'in', ('draft', 'waiting', 'confirmed', 'assigned')),
                ('product_id', '=', self.product_id.id),
                ('picking_id.purchase_id', '=', recPO.id),
                ('product_uom_qty', '>', 0)]
        needed = len(self.move_line_ids)
        lines = self.move_line_ids.filtered(lambda l:
                        not l.ref_auto_stock_move_line)
        current = 0
        for recForeignSM in self.search(args):
            maxQty = recForeignSM.product_uom_qty
            pos = 0
                        # - Luego por cada una de las cantidades mientras sea menor que 
                        # las cantidades del Albarán de Ventas pasar el número de serie,
                        # es decir, crear un move line con el serial number
            while maxQty > pos and needed > current:
                lines[current]._propagate_stock_move_line(recForeignSM)
                pos += 1
                current += 1
                recPicking |= recForeignSM.picking_id
        return recPicking


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    ref_auto_stock_move_line = fields.Many2one('stock.move.line',
            string='From another company', readonly=True, copy=False)

    def _propagate_stock_move_line(self, recForeignSM):

        # recPO = self.sale_id.auto_purchase_order_id
        # argsSP = [('state', '=', 'draft'), ('purchase_id', '=', recPO.id)
        #         ('company_id', '!=', self.env.user.company_id.id)]
        # recPick = self.env['stock.picking'].search(argsSP)
        # argsSM = [('picking_id', 'in', recPick.ids),
        #         ('product_id', '=', self.product_id.id)]
        # recMove = self.env['stock.move'].search(argsSM)

        vals = self._prepare_sml_values(recForeignSM)
        lines = recForeignSM.move_line_ids.filtered(lambda ml: not ml.lot_id)
        if lines:
            recNewSML = lines[0]
            recNewSML.write({
                'lot_id': vals.get('lot_id'),
                'lot_name': vals.get('lot_name'),
                'qty_done': 1,
            })
        else: recNewSML = self.env['stock.move.line'].create(vals)
        self.write({'ref_auto_stock_move_line': recNewSML.id})

        # Crear un move line por cada serie del producto
        # Hacerlo mejor por Stock Moves
            # Luego busco las líneas del Stock.move
            # Busco el Stock.Move del Purc vchase que se ajusta al Producto
            # y por cada línea con Lote creo una nueva en el Picking del Purchase
            # con el mismo número de serie


    def _prepare_sml_values(self, recForeignSM):
        recLot = self._create_lot_id(recForeignSM)
        return {
            'move_id': recForeignSM.id,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'lot_name': recLot.name,
            'lot_id': recLot.id,
            'product_uom_qty': 1,
            'qty_done': 1,
            'location_id': self.picking_id.location_id.id,
            'location_dest_id': self.picking_id.location_dest_id.id,
            'company_id': recForeignSM.company_id.id,
            'ref_auto_stock_move_line': self.id,
            'picking_id': recForeignSM.picking_id.id,
        }

    def _create_lot_id(self, recForeignSM):
        vals = self._prepare_serial_lot(recForeignSM)
        recLot = self.env['stock.production.lot'].create(vals)
        return recLot

    def _prepare_serial_lot(self, recForeignSM):
        return {
            'name': self.lot_id.name,
            'product_id': self.product_id.id,
            'company_id': recForeignSM.company_id.id,
        }
