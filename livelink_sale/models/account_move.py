from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    is_dealer = fields.Boolean('Cancelar envío de notificaciones',
            help='''
                No enviar Facturas por correo al Cliente.
                Por defecto se muestra marcado para los COncesionarios
            ''')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id: self.is_dealer = self.partner_id.is_dealer
        return super(AccountMove, self)._onchange_partner_id()
