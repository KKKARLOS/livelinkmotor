from odoo import api, models, fields

class Services(models.Model):
    _name = 'services'
    _description = "Catalogo de servicios"

    name = fields.Char(string="Nombre")