from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    x_studio_num_serial = fields.Char(
        string='Num Serial',
        related='picking_id.product_lot.display_name'
    )
