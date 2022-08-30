from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_studio_clasificacin_compras = fields.Selection(
        string="Clasificación compras",
        selection=[
            ('Componentes electrónicos', 'Componentes electrónicos'),
            ('Materia Prima', 'Materia Prima'),
            ('Consumibles', 'Consumibles'),
            ('Transporte', 'Transporte'),
            ('General', 'General'),
            ('Servicios', 'Servicios'),
        ],
        help="Seleccionar el tipo de producto que se está comprando para su "
             "posterior clasificación"
    )
