# -*- coding: utf-8 -*-
from email.policy import default
from odoo import api, fields, models, _
from odoo.exceptions import Warning


VIRTUAL_STATES = [('confirmed', 'Confirmed'), ('unconfirmed', 'Unconfirmed'), ('created', 'Created')]

class StockProdVirtualLot(models.Model):
    _name = 'stock.production.virtual.lot'
    _order = 'intercompany_move_line_id desc, intercompany_ext_lot_id desc'

    name = fields.Char('Serial number', required=True)
    state = fields.Selection(VIRTUAL_STATES, 'States', default='unconfirmed')
    product_id = fields.Many2one('product.product', string='Product')
    intercompany_move_id = fields.Many2one('stock.move',
            string='Stock move from external company')
    intercompany_ext_sale_id = fields.Many2one('sale.order',
            string='Stock sale order from external company')
    intercompany_ext_lot_id = fields.Many2one('stock.production.lot',
            string='Stock production lot from external company')
    intercompany_move_line_id = fields.Many2one('stock.move.line',
            string='Stock move line from external company')

    @api.model
    def create(self, vals):
        if (not 'state' in vals or vals.get('state') == 'unconfirmed'):
            recExtLot = self.check_exist_another_company(vals)
            if recExtLot:
                vals.update({
                    'state': 'confirmed',
                    'intercompany_ext_lot_id': recExtLot.id,
                })
        return super(StockProdVirtualLot, self).create(vals)

    def write(self, vals):
        if (('state' in vals and vals.get('state') == 'unconfirmed') \
                or self.mapped('state') == 'unconfirmed') or vals.get('name'):
            recExtLot = self.check_exist_another_company(vals)
            if recExtLot:
                vals.update({
                    'state': 'confirmed',
                    'intercompany_ext_lot_id': recExtLot.id,
                })
        return super(StockProdVirtualLot, self).write(vals)

    def check_exist_another_company(self, vals):
        cids = self.env['res.company'].sudo().search([]).ids
        super_self = self.with_context(allowed_company_ids=cids)
        return super_self.check_exist_another_in_all_companies(vals)

    def check_exist_another_in_all_companies(self, vals):
        name = self._get_name(vals)
        if not name: return False

        recProduct = self._get_product(vals)
        if not recProduct: return False

        recMove = self._get_stock_move(vals)
        if not recMove: return False

        recSale = self._get_external_sale(vals, recMove)
        if not recSale: return False

        args = [
            ('product_qty', '>', 0), ('name', '=', name),
            ('company_id', '=', recSale.company_id.id),
            ('product_id', '=', recProduct.id)
        ]
        return self.env['stock.production.lot'].search(args, limit=1)
    
    def _get_name(self, vals):
        name = False
        if self.id and self.name: name = self.name
        if vals.get('name'): name = vals.get('name')
        return name or False

    def _get_product(self, vals):
        if self.id and self.product_id: return self.product_id
        product = False
        if vals.get('product_id'): product = vals.get('product_id')
        elif self._context.get('default_product_id'):
            product = self._context.get('default_product_id')
        if not product: return False
        return self.env['product.product'].browse(product)

    def _get_stock_move(self, vals):
        move_id = False
        if vals.get('intercompany_move_id'):
            move_id = vals.get('intercompany_move_id')
        elif self._context.get('default_intercompany_move_id'):
            move_id = self._context.get('default_intercompany_move_id')
        elif self._context.get('intercompany_move_id'):
            move_id = self._context.get('intercompany_move_id')
        if move_id: return self.env['stock.move'].browse(move_id)
        if self.id: return self.intercompany_move_id or False
        return False

    def _get_ext_sale_order(self, mypurchase):
        args = [
            ('auto_purchase_order_id', '=', mypurchase.id),
            ('state', 'in', ['sale', 'done'])
        ]
        recSO = self.env['sale.order'].search(args, limit=1)
        return recSO or False

    def _get_external_sale(self, vals, recMove=False):
        if vals.get('intercompany_ext_sale_id'):
            return vals.get('intercompany_ext_sale_id')
        
        if recMove:
            recPO = recMove.purchase_line_id.order_id
            if recPO:
                sale = self._get_ext_sale_order(recPO)
                if sale: vals.update({'intercompany_ext_sale_id': sale.id})
                return sale

        return False