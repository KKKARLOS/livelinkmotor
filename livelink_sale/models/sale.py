from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_processed = fields.Boolean('¿Tramitado?')
    is_dealer = fields.Boolean('Cancelar envío de notificaciones',
            help='''
                No enviar Facturas por correo al Cliente.
                Por defecto se muestra marcado para los COncesionarios
            ''')

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id: self.is_dealer = self.partner_id.is_dealer
        return super(SaleOrder, self).onchange_partner_id()

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        if self.auto_workflow_process_id:
            if self.auto_workflow_process_id.invoice_date_is_order_date:
                invoice_vals['date'] = self.date_order.date()
                # Pedido por Javier de Contabilidad
                #invoice_vals['invoice_date'] = fields.Date.context_today(self)
                invoice_vals['invoice_date'] = self.date_order.date()
        invoice_vals['is_dealer'] = self.is_dealer
        return invoice_vals
