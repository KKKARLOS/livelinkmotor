# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import Warning


class res_company(models.Model):
    _inherit = 'res.company'

    auto_propagate_serials = fields.Boolean(string="Automatic Send Serials")


class LnkPortalWizardUser(models.TransientModel):
    _inherit = 'portal.wizard.user'

    company_id = fields.Many2one(related='user_id.company_id')
