# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import timedelta

class ClientType(models.Model):
    _name = 'client.type'
    name = fields.Char(string='Nombre')

class ServiceLine(models.Model):
    _name = 'service.line'

    fecha_inicio = fields.Date(string='Fecha inicio')
    fecha_fin = fields.Date(string='Fecha fin')
    time1 = fields.Integer(string='Tiempo(meses)', related="subscription.catalog_ids.meses")
    subscription = fields.Many2one('subscription', string='Suscripcion')
    aws_subscription = fields.Many2one('aws.subscriptions', string='Referencia')

class AwsSubscriptions(models.Model):
    _name = 'aws.subscriptions'
    _description = 'AWS Subscription'

    name = fields.Char(copy=False, string='Referencia', readonly=True, default='New')
    serial_number = fields.Many2one('stock.production.lot', string='Numero Serie')
    imei1 = fields.Many2one('aws.device', string='IMEI')
    mac1 = fields.Many2one('aws.key', string='MAC')
    iccid = fields.Many2one('aws.device.iccid', string='ICCID', related='imei1.icc_id')
    num_pedido = fields.Many2one('sale.order', string='Numero Pedido')
    type_client = fields.Many2one('client.type', string='Tipo Cliente')
    product = fields.Many2one('product.product', string='Producto', related='serial_number.product_id')
    efectiv_date = fields.Date(string='Fecha Efectiva', related='num_pedido.effective_date')
    aws_firmware = fields.Many2one('aws.firmware', string='Firmware', related='imei1.firmware_id')
    instalation_date = fields.Date(string='Fecha Instalacion', related='num_pedido.effective_date')
    user_email = fields.Char(string='User Email', related='num_pedido.partner_id.email')
    services = fields.One2many('subscription', string='Subscripciones', related='product.product_tmpl_id.subscriptions_ids')
    services_line = fields.One2many('service.line', string="Servicios", inverse_name="aws_subscription")
    historial = fields.One2many('history', inverse_name='referencia', string="Historial")

    # Datos clientes"
    # TODO Faltan datos de compra:  fecha pedido, y cupón.
    client_id = fields.Many2one('res.partner', string="Cliente", related="num_pedido.partner_id")
    fecha_pedido = fields.Datetime(string="Fecha de pedido", related="num_pedido.date_order")
    direct_ent = fields.Many2one('res.partner', string="Direccion de entrega", related="num_pedido.partner_shipping_id")
    direct_fact = fields.Many2one('res.partner', string="Direccion de factura", related="num_pedido.partner_invoice_id")

    @api.model
    def create(self,vals):
        if vals.get('name','New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('task.1fpv') or 'New'
            result = super(AwsSubscriptions,self).create(vals)
            return result

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def get_services(self, ref):
        for service in ref.services:
            if service.catalog_ids.meses > 0:
                fecha_fin = service.fecha_activacion + timedelta(days=30 * service.catalog_ids.meses)
            else:
                fecha_fin = service.fecha_activacion
            serviceAux = self.env['service.line'].create({'subscription': service.id, 'aws_subscription': ref.id,
                                                          'fecha_inicio': service.fecha_activacion, 'fecha_fin': fecha_fin})
            ref.services_line += serviceAux

    def button_validate(self):
        super().button_validate()
        if self.state == 'done':
            for product in self.move_line_nosuggest_ids:
                if product.lot_id != False:
                    serialnum = product.lot_id
                    qualitiesAux = self.env['quality.check'].search_read([['finished_lot_id.name', '=', serialnum.name]])
                    mac = None
                    imei = None
                    for quality in qualitiesAux:
                        if 'DEV' in quality['component_id'][1]:
                            imei = self.env['aws.device'].search_read([['name', '=', quality['lot_id'][1]]])
                        if 'KEY' in quality['component_id'][1]:
                            mac = self.env['aws.key'].search_read([['name', '=', quality['lot_id'][1]]])
                    if mac == None:
                        service = self.env['aws.subscriptions'].create(
                            {'serial_number': serialnum.id, 'imei1': imei[0]['id'],
                             'num_pedido':self.sale_id.id})
                        self.get_services(service)
                        albaran = self.env['stock.picking'].search_read([['sale_id', '=', service.num_pedido.id]])
                        self.env['history'].create({'referencia': service.id,
                                                    'activo': True, 'albaran': albaran[0]['id'], 'order': 'sal',
                                                    'imei_mac': imei[0]['imei_id'][0]})
                    elif imei == None:
                        service = self.env['aws.subscriptions'].create(
                            {'serial_number': serialnum.id, 'mac1': mac[0]['id'],
                             'num_pedido': self.sale_id.id})
                        self.get_services(service)
                        albaran = self.env['stock.picking'].search_read([['sale_id', '=', service.num_pedido.id]])
                        self.env['history'].create(
                            {'referencia': service.id, 'activo': True
                             , 'albaran': albaran[0]['id'], 'order': 'sal','imei_mac': mac[0]['imei_id'][0]})
                    else:
                        service = self.env['aws.subscriptions'].create(
                            {'serial_number': serialnum.id, 'imei1': imei[0]['id'], 'mac1': mac[0]['id'],
                             'num_pedido': self.sale_id.id})
                        self.get_services(service)
                        albaran = self.env['stock.picking'].search_read([['sale_id', '=', service.num_pedido.id]])
                        self.env['history'].create(
                            {'referencia': service.id, 'activo': True, 'albaran': albaran[0]['id']
                             , 'order': 'sal', 'imei_mac': imei[0]['imei_id'][0]})
                        self.env['history'].create(
                            {'referencia': service.id, 'activo': True, 'albaran': albaran[0]['id']
                             , 'order': 'sal', 'imei_mac': mac[0]['mac_id'][0]})




class History(models.Model):
    _name = 'history'

    referencia = fields.Many2one('aws.subscriptions', string="Referencia")
    imei_mac = fields.Many2one('stock.production.lot', string='Mac/Imei')
    fecha = fields.Date(string="Fecha")
    albaran = fields.Many2one('stock.picking', string="Albarán", computed="get_albaran")
    activo = fields.Boolean(string="Activo")
    order = fields.Selection(string="Orden", selection= [('ent', 'Etrada'), ('sal', 'Salida')])

    def get_albaran(self):
        sale = self.env['stock.picking'].search_read([['sale_id', '=', self.referencia.num_pedido]])
        self.activo = sale[0]['id']

# Introducir fecha instala
# ción, y partner (user email) desde AWS dado un IMEI.
# Casos: que pasa si AWS intenta meter un partner en un IMEI que ya tiene uno.
# TODO Añadir una suscripción extra
# TODO Crear pestaña Historial: Añadir los dos albaranes de salida de dispositivo y llavero en el momento de salida. SIN DEVOLUCIONES