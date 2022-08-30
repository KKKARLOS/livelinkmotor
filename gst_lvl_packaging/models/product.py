from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    type_app = fields.Selection([('city', 'City'), ('pro', 'Pro')], string='Type App',store=True)
    months_suscription = fields.Integer(string='Months Suscriptions')
    language = fields.Many2one('language', string='Lenguaje')

