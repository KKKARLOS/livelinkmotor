from datetime import datetime, date, timedelta
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger('Model AWS Subscription')


STATES = [
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('validated', 'Validated'),
    ('open', 'Register')
]
class LvlAwsSubscription(models.Model):
    _name = 'aws.subscription.history'
    _rec_name = 'imei'

    imei = fields.Char('IMEI')
    email = fields.Char('Email')
    date = fields.Date('Install date')
    registration_date = fields.Datetime('Registration',
            default=fields.Datetime.now())
    state = fields.Selection(STATES, default='new')
    lot_id = fields.Many2one('stock.production.lot', string='IMEI number')
    serial_id = fields.Many2one('stock.production.lot', string='Serial number')

    first_sale_id = fields.Many2one('sale.order', string='First sale')
    last_sale_id = fields.Many2one('sale.order', string='Last sale')

    def action_run_process(self):
        # Obtain stock.production.lot
        self.search([('state', '=', 'new')])._get_locate_product_imei()
        self.search([('state', '=', 'in_progress')])._get_final_product()

    def _get_locate_product_imei(self):
        for record in self:
            args = [('name', '=', record.imei)]
            recIMEI = self.env['aws.device'].search(args)
            if recIMEI:
                record.write({
                    'lot_id': recIMEI.imei_id.id,
                    'state': 'in_progress',
                })

    def _get_final_product(self):
        for record in self:
            # Buscar los movimientos del IMEI'
            # espejo creado automáticamente
            recSML = record._get_stock_move_line()

            # Buscar donde fue consumido como componente
            while recSML and recSML.mapped('production_id'):
                auxL = recSML.mapped('production_id.finished_move_line_ids')
                if auxL and len(auxL) == 1: recSML = auxL
                else: _logger.info(f'===> Problemas con la TRAZABILIDAD')

            if recSML:
                values = {}
                # Si no fue consumido entonces es que ha sido vendido
                sale_id = recSML._get_sale_order()
                if sale_id and sale_id[0]:
                    values.update({
                        'serial_id': recSML.lot_id.id,
                        'first_sale_id': sale_id[0].get('id')
                    })
                last_sale_id = recSML._get_last_sale_order()
                if last_sale_id and last_sale_id[0]:
                    values.update({'last_sale_id': last_sale_id[0].get('id')})
                if sale_id and last_sale_id: values.update({'state': 'validated'})
                record.write(values)

    def _get_stock_move_line(self):
        self.ensure_one()
        objSML = self.env['stock.move.line']
        #pname = 'gst_lvl_connector_aws.product_product_device_imei'
        args = [
            ('lot_id.name', '=', self.lot_id.name),
            #('product_id', '!=', self.env.ref(pname).id),
            ('product_id', '!=', self.lot_id.product_id.id),
            ('company_id', '=', self.lot_id.company_id.id)
        ]
        return objSML.search(args)

    def run_subscription(self):
        """Insert Subscription history"""
        result = []
        data = [r for r in self.ids]
        _logger.info(f'=== INSERT Subscription: {data}')
        if data:
            try:
                result = self.create(data)
            except Exception as e:
                _logger.info(str(e))
                raise e
        return len(result) and result.ids or -1
