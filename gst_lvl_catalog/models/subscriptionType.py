from odoo import api, models, fields

class SubscriptionType(models.Model):
    _name = 'subscription.type'
    _description = "Master subscription type"

    name = fields.Char(string='Nombre')
    identificador = fields.Char(string='Identificador', size=5)
    catalog_subs = fields.One2many('catalog.subscription', inverse_name='subscription_type', string='Catalogo subs')


