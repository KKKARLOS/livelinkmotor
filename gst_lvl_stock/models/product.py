from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.template'

    sequence_id = fields.Many2one(
        comodel_name='ir.sequence',
        string='Sequencia',
    )
