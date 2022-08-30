from odoo import fields, models


class Sequence(models.Model):
    _inherit = 'ir.sequence'

    product_ids = fields.One2many(
        comodel_name='product.template',
        inverse_name='sequence_id',
        string='Products'
    )
