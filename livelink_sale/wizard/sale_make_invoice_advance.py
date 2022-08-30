from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super(SaleAdvancePaymentInv)._prepare_invoice_values(
                                            order, name, amount, so_line)
        if hasattr(order, 'is_dealer'): res['is_dealer'] = order.is_dealer
        return res
