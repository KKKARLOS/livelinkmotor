from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    x_studio_field_JeUHm = fields.Binary(
        string="New Imagen",
    )
    x_studio_logo_marca = fields.Binary(
        string="logo_marca",
    )
    x_studio_logo_marca_1 = fields.Binary(
        string="logo_marca",
    )
