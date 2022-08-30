from odoo import api, models, fields

class Subscription(models.Model):
    _name = 'subscription'
    _description = "Subscription"

    name = fields.Char(string='Nombre')
    fecha_activacion = fields.Date(string='Fecha activacion')
    fecha_desactivacion = fields.Date(string='Fecha desactivacion',)
    products_ids = fields.Many2one('product.template', string='Producto')
    catalog_ids = fields.Many2one('catalog.subscription', string='Catalogo suscripción')
