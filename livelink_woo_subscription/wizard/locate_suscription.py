# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
import locale

from odoo import api, fields, models
from odoo.exceptions import UserError


class LvlVirtualSubscription(models.TransientModel):
    _name = 'virtual.subscription.imei'

    seq = fields.Integer(string='', readonly=True)
    name_product_subs = fields.Char('Services', readonly=True)
    description_sale_subs = fields.Char('Services', readonly=True)
    aws_subs_id = fields.Many2one('aws.subscription.history', 'IMEI')
    subs_line_id = fields.Many2one('sale.subscription.line', 'Subs line')

    def _create_subscription(self):
        recLine = self._get_current_line_subscription()
        if not recLine:
            recP = self._get_current_partner()
            recSubs = self._get_clone_subscription()
            recSubs.write({'partner_id': recP.id})
            if recSubs == self.subs_line_id.analytic_account_id:
                recLine = self.subs_line_id
            else: 
                recLine = self.subs_line_id.copy({
                    'analytic_account_id': recSubs.id,
                    'quantity': 1
                })
                self.subs_line_id.write({'quantity': recLine.quantity - 1})
        recLine.analytic_account_id.write({
            'imei_id': self.aws_subs_id.lot_id.id,
            'serial': self.aws_subs_id.serial_id.id,
            'install_date': self.aws_subs_id.date,
        })
        recLine.write({
            'start_date': self.aws_subs_id.date,
            'end_date': self.aws_subs_id.date +timedelta(days=90),
        })
        self.aws_subs_id.state = 'open'
        # ToDo: You can do it better. Wrong many2one in sale.order
        oldS = self.subs_line_id.analytic_account_id
        newS = recLine.analytic_account_id
        if oldS != newS:
            argsO = [('subscription_id', '=', oldS.id)]
            recSOL = self.env['sale.order.line'].search(argsO)
            if recSOL: recSOL.write({'subscription_id': newS.id})
        return recLine.analytic_account_id

    def _get_current_line_subscription(self):
        recLine = False
        argsS = [('in_progress', '=', True)]
        recStages = self.env['sale.subscription.stage'].search(argsS)

        args = [('partner_id.email', '=', self.aws_subs_id.email),
                ('stage_id', 'in', recStages.ids)]
        recSubs = self.env['sale.subscription'].search(args, limit=1)
        if recSubs:
            recLine = self.subs_line_id.copy({
                'analytic_account_id': recSubs.id
            })
        return recLine

    def _get_current_partner(self):
        objP = self.env['res.partner']
        recP = objP.search([('email', '=', self.aws_subs_id.email)], limit=1)
        if not recP:
            recP = objP.create({
                        'name': self.aws_subs_id.email,
                        'email': self.aws_subs_id.email
                    })
        return recP

    def _get_clone_subscription(self):
        subs = self.subs_line_id.analytic_account_id
        return subs if len(subs.recurring_invoice_line_ids) == 1 \
                and subs.recurring_invoice_line_ids == self.subs_line_id \
                and self.subs_line_id.quantity == 1 \
            else subs.copy({'recurring_invoice_line_ids': False})


class LvlLocateSubscription(models.TransientModel):
    _name = 'locate.subscription'
    _description = 'Schedule task'

    sale_subs_line_id = fields.Many2one('sale.subscription.line')
    lines = fields.Many2many('virtual.subscription.imei')

    @api.model
    def default_get(self, fields):
        res = super(LvlLocateSubscription, self).default_get(fields)
        args = [('id', 'in', self.env.context.get('active_ids'))]
        recLine = self.env['sale.subscription.line'].search(args, limit=1)
        res['lines'] = [(0,0, {
                            'seq': pos+1,
                            'name_product_subs': recLine.product_id.name,
                            'description_sale_subs': recLine.name,
                            'subs_line_id': recLine.id,
                        }) for pos in range(int(recLine.quantity))]
        return res

    def action_assign_service(self):
        [subscription._create_subscription()
            for subscription in self.lines if subscription.aws_subs_id]
        args = [('id', 'in', self.env.context.get('active_ids'))]
        recLine = self.env['sale.subscription.line'].search(args, limit=1)
        subs_id = recLine.analytic_account_id
        if not recLine.quantity \
                and len(subs_id.recurring_invoice_line_ids) == 1:
            subs_id.write({'stage_id': 4})
