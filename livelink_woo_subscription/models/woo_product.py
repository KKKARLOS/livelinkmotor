from curses import keyname
from datetime import datetime, date, timedelta

import json
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger("Livelink -> Woo")


MAP_CASTS = {'price': 'double'}
MAP_NAMES = {
    'period_interval': 'recurring_interval',
    'period': 'recurring_rule_type',
    'limit': 'recurring_rule_boundary',
    'price': 'list_price',
}
PROD_FIELDS = ['list_price']
NEED_MAP_FIELDS = {
    'limit': {'no': 'unlimited', 'active': 'unlimited', 'any': 'unlimited'},
    'period': {'day': 'daily', 'week': 'weekly',
                'month': 'monthly', 'year': 'yearly'}
}
VALID_FIELDS = ['limit', 'period', 'period_interval', 'price']

class LvlWooProductTemplateEpt(models.Model):
    _inherit = 'woo.product.template.ept'

    @api.model
    def sync_products(self, product_data_queue_lines, woo_instance,
                        common_log_book_id, skip_existing_products=False,
                        order_queue_line=False):
        subs = {}
        [subs.update(self._set_subscription_to_simple(extProduct))
            for extProduct in product_data_queue_lines if not order_queue_line]
        res = super(LvlWooProductTemplateEpt, self).sync_products(
                    product_data_queue_lines, woo_instance, common_log_book_id,
                    skip_existing_products, order_queue_line)
        [self._force_change_subscription(k, subs.get(k)) for k in subs.keys()]
        return res

    def _set_subscription_to_simple(self, ext_product):
        vals = {}
        data = json.loads(ext_product.woo_synced_data)
        if data and data.get('type') == 'subscription':
            sku = data.get('sku')
            name = "[%s] %s" % (sku, data.get('name'))
            info_subs = data.get('meta_data')

            msg0 = "Identificado Producto Suscripción {0}".format(name)
            _logger.info("{0}".format(msg0))
            
            if sku:
                data['type'] = 'simple'
                aux = json.dumps(data)
                ext_product.woo_synced_data = aux
                vals = {sku: info_subs}
        return vals

    def _force_change_subscription(self, sku, subscription):
        args = [('default_code', '=', sku)]
        recProd = self.env['product.template'].search(args)
        if recProd:
            data = self._mapped_meta_data(subscription)
            self._update_product(recProd, data)
            recSubs = self._get_subscription(data)
            recProd.write({
                'type': 'service',
                'recurring_invoice': True,
                'subscription_template_id': recSubs.id or 1
            })
            name = "[%s] %s" % (sku, recProd.name)
            msg0 = "Transformado Producto en Suscripción {0}".format(name)
            _logger.info("{0}".format(msg0))

    def _get_subscription(self, data):
        objSubs = self.env['sale.subscription.template']
        limit = data.get('recurring_rule_boundary')
        args = [('recurring_interval', '=', data.get('recurring_interval')),
                ('recurring_rule_type', '=', data.get('recurring_rule_type')),
                ('recurring_rule_boundary', '=', limit)]
        recSubs = objSubs.search(args)
        if not recSubs: recSubs = self._create_subscription(data)
        return recSubs

    def _create_subscription(self, meta_data):
        objSubs = self.env['sale.subscription.template']
        _interval = meta_data.get('recurring_interval')
        _period = meta_data.get('recurring_rule_type')
        name = ''
        if int(_interval) > 1: name += 'Each %s' % _interval
        meta_data.update({
            'name': "{0} {1} Subscription".format(name, _period.capitalize()),
            'user_closable': True,
           # 'auto_close_limit': 10, # Review and ToDo
            'payment_mode': 'manual', # Review and ToDo
            'company_id': self.woo_instance_id.company_id.id,
        })
        #meta_data.pop('list_price')
        return objSubs.create(meta_data)

    def _mapped_meta_data(self, subscription):
        map_keys = [*NEED_MAP_FIELDS.keys()]
        data = {}
        for s in subscription:
            key_name = s.get('key').replace('_subscription_', '')
            if key_name in VALID_FIELDS:
                value = NEED_MAP_FIELDS.get(key_name).get(s.get('value')) \
                            if key_name in map_keys else s.get('value')
                if key_name in MAP_CASTS:
                    if MAP_CASTS.get(key_name) == 'double':
                        value = float(value)
                data.update({MAP_NAMES.get(key_name): value})
        return data

    def _update_product(self, recProd, data):
        vals = {}
        aux = dict(data)
        for k in aux.keys():
            if k in PROD_FIELDS:
                vals.update({k: data.pop(k)})
        recProd.write(vals)