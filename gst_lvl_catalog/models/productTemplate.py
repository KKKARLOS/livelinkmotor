from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    subscriptions_ids = fields.One2many('subscription', inverse_name='products_ids', string='Suscripciones')

