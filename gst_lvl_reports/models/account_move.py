# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_sale_order_data(self):
        for rec in self:
            orders = self.env['sale.order'].search([(
                'order_line.invoice_lines.move_id', '=', rec.id)], limit=1)
        return orders