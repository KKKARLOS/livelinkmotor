from datetime import datetime, date, timedelta

from odoo import api, fields, models, _


class LvlSubsPartnerType(models.Model):
    _name = 'sale.subscription.partner.type'

    name = fields.Char('Name')


class LvlSubsApp(models.Model):
    _name = 'sale.subscription.app'

    name = fields.Char('Name App')


class LvlSaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    imei_id = fields.Many2one('stock.production.lot', string='IMEI serial')
    mac_id = fields.Many2one('stock.production.lot', string='MAC serial')
    serial = fields.Many2one('stock.production.lot', string='Serial Number')
    order_date = fields.Date('Order date')
    install_date = fields.Date('Install date')
    customer_type = fields.Many2one('sale.subscription.partner.type',
            string='Customer type')
    app_name = fields.Many2one('sale.subscription.app', string='App name')


class LvlSaleSubscriptionLine(models.Model):
    _inherit = 'sale.subscription.line'

    start_date = fields.Date('Start date')
    end_date = fields.Date('End date')
    aws_subs_id = fields.Many2one('aws.subscription.history')
