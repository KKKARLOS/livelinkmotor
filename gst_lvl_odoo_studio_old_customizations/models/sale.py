from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_studio_correo_electrnico = fields.Char(
        string='Correo electrónico',
    )
