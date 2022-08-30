from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    x_studio_producto = fields.Selection(
        string='Producto',
        selection=[
            ('Device', 'Device'),
            ('Key', 'key'),
        ],
    )


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    x_studio_field_h2z6u = fields.One2many(
        comodel_name='mrp.workorder',
        inverse_name='workcenter_id',
        string='New UnoAMuchos',
    )
