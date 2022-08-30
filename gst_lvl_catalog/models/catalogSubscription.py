from odoo import api, models, fields

class CatalogSubscription(models.Model):
    _name = 'catalog.subscription'
    _description = "Catalogo subscripciones"

    name = fields.Char(string='Nombre')
    meses = fields.Integer(string='Meses')
    aux_type = fields.Char(string="Aux Type", related="subscription_type.identificador")
    service_id = fields.Many2one('services', string="Catalogo Servicio")
    subscription_type = fields.Many2one('subscription.type', string='Tipos Sub')
    subscriptions_ids = fields.One2many('subscription', inverse_name='catalog_ids', string='Suscripciones')



