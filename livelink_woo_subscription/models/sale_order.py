from datetime import datetime, date, timedelta

from odoo import api, fields, models, _


class LvlSaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_subscription_data(self, template):
        res = super(LvlSaleOrder, self)._prepare_subscription_data(template)
        objStage = self.env['sale.subscription.stage']
        default_stage = objStage.search([('in_progress', '=', False)], limit=1)
        res['stage_id'] = default_stage and default_stage.id or False
        return res

    @api.model
    def create_woo_order_line(self, line_id, product, quantity, order, price,
                        taxes, tax_included, woo_instance, is_shipping=False):
        recSOL = self.env['sale.order.line']
        if product.type != 'service' or not product.recurring_invoice: rows = 1
        else: rows, quantity = quantity, 1
        for q in range(int(rows)):
            recSOL |= super(LvlSaleOrder, self).create_woo_order_line(line_id,
                                    product, quantity, order, price, taxes,
                                    tax_included, woo_instance, is_shipping)
        return recSOL


class LvlSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_subscription_line_dataX(self):
        """Prepare a dictionnary of values to add lines to a subscription."""
        values = list()
        for line in self:
            mgmt_subs = line.order_id.subscription_management
            discount = line.discount if mgmt_subs != 'upsell' else False
            quantity = int(line.product_uom_qty) or 1
            for q in range(quantity):
                values.append((0, False, {
                    'product_id': line.product_id.id,
                    'name': line.name,
                    'quantity': 1,
                    'uom_id': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'discount': discount,
                }))
        return values
