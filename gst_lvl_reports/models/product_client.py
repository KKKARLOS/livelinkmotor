from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    tradename = fields.Char(string='Nombre comercial')