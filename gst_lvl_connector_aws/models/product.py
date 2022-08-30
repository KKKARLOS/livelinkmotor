from odoo import fields, models

class Product(models.Model):
    _inherit = 'product.template'

    is_device = fields.Boolean(string='is Device?', default=False)
    is_key = fields.Boolean(string='is Key?', default=False)
