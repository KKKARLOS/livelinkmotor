
from odoo import _, api, models, fields

class Languaje(models.Model):
    _name = "language"

    name = fields.Char(string='Lenguaje')

