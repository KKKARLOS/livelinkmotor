from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_dealer = fields.Boolean('Is dealer?', default=False)
