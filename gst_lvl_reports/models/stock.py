from odoo import api, models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    product_lot = fields.Many2one(comodel_name='stock.production.lot')