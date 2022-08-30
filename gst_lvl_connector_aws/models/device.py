# -*- encoding: utf-8 -*-
#    Guadaltech Soluciones tecnológicas S.L.  www.guadaltech.es
#    Author: Guadaltech Soluciones Tecnológicas S.L.
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
from odoo import fields, models
from odoo.exceptions import UserError
# from livelink.gst_lvl_connector_aws.auxiliary.sync_datatime_zone \
#     import sync_datetime_zone

from odoo.addons.gst_lvl_connector_aws.auxiliary.sync_datatime_zone \
    import sync_datetime_zone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar

import logging

_logger = logging.getLogger(__name__)

SELECTION_FIELDS = [('OK', 'Ok'), ('NOK', 'Not Ok')]

class AwsDeviceSuscripcions(models.Model):
    _name = 'aws.device.suscripcions'
    _description = 'AWS Device Suscripcions'

    code = fields.Char('Code')
    num_months = fields.Integer('Num Months')
    device_id = fields.Many2one('aws.device', string='Device')


class AwsDevice(models.Model):
    _name = 'aws.device'
    _description = 'AWS Device'

    #_rec_name = 'imei'

    name = fields.Char('IMEI', related='imei_id.name')
    #imei = fields.Char('IMEI', required=True)
    imei_id = fields.Many2one('stock.production.lot', string='IMEI serial',
                              required=True)
    company_id = fields.Many2one(related='imei_id.company_id')
    iccid = fields.Char('ICCID', related='icc_id.name')
    icc_id = fields.Many2one('aws.device.iccid', string='ICCID', required=True)
    assembledOn = fields.Datetime(string='Assembled on', required=True)
    status = fields.Selection(SELECTION_FIELDS, 'Bootstrapping', required=True)
    firmware_id = fields.Many2one('aws.firmware', string='Firmware')
    partner_id = fields.Many2one('res.partner', string='Partner')
    history_ids = fields.One2many('aws.device.history', 'device_id', 'History')
    devicePcbId = fields.Char('devicePcbId')
    #==========================================================================
    # , related='pcb_id.name'
    # pcb_id = fields.Many2one('stock.production.lot', string='PCB serial',
    #                           required=True)
    #==========================================================================
    device_test_ids = fields.One2many(
        comodel_name='aws.device.test',
        inverse_name='device_id',
        string='Device Tests'
    )
    state = fields.Selection(
        selection=[
            ('new', 'Nuevo'),
            ('validated', 'Validado'),
            ('programmed', 'Programado'),
            ('finished', 'Terminado'),
            ('registered', 'Registrado'),
        ],
        default='new'
    )
    app_type = fields.Selection(
        selection=[('city', 'City'), ('pro', 'Pro'),],
        string="App type"
    )
    subscription_time = fields.Integer(string='Subscription time')

    suscripcions_ids = fields.One2many('aws.device.suscripcions', 'device_id',
        string='Suscriptions')
    product_id = fields.Many2one('product.product', string='Product')
    failed_qa_test = fields.Boolean('Invalid test?', compute='_compute_invalid_QA_test')

    def _compute_invalid_QA_test(self):
        for rec in self:
            rec.failed_qa_test = any([t for t in rec.device_test_ids
                                        if t.status != 'OK'])
            if not rec.device_test_ids: rec.failed_qa_test = True

    #TODO Make constrain imei unique. ¿devicePcbId, may be?

    def get_device_id_by_imei(self, imei):
        """Returns the device id matching imei's value"""
        return self.search([('name', '=', imei)], limit=1)

    def get_device_by_device_pcbid(self, devicePcbId):
        return self.search([('devicePcbId', '=', devicePcbId)], limit=1)



    def insert_device(self):
        """Insert device. This action it's known as 'Bootstrapping'.
        TODO: describe params"""
        result = []
        obj_lot = self.env['stock.production.lot']
        iccid_obj = self.env['aws.device.iccid']
        data = [record for record in self.ids
                if not self.get_device_id_by_imei(record.get('imei'))]
        if self and not len(data): return True
        _logger.info(f'=== INSERT DEVICE: {data}')
        if data:
            for device in data:
                on_date = device.get('assembledOn', False)
                if on_date:
                    device['assembledOn'] = sync_datetime_zone(on_date)
                iccid = device.get('iccid', False)
                if iccid:
                    iccid_id = iccid_obj.create({'name': iccid})
                    device['icc_id'] = iccid_id and iccid_id.id
                obj_lot._add_serial_number(device, True) 
            try:
                result = self.create(data)
                _logger.info(f'=== INSERT DEVICE: DONE')
                _logger.info('=== FIX iccid with current_device')
                for device in result:
                    if device.icc_id:
                        device.icc_id.write({'device_id': device.id})
                    if device.imei_id:
                        device.imei_id.write({'device_id': device.id})
            except Exception as e:
                _logger.info(f'=== INSERT DEVICE: FAIL')
                _logger.info(str(e))
                print(str(e))
                raise e
        return len(result) and result.ids or -1

    #llamada externa por WS
    def setSuscripcionCodeNoSetup(self, code, imei_name, num_months, product_code):
        if imei_name:
            imei_id = self.get_device_id_by_imei(str(imei_name))
            if not imei_id.partner_id:
                return False
            else:
                if product_code:
                    product_id = self.env['product.product'].search([('default_code','=',str(product_code))])
                    if product_id:
                        self.write({'product_id':product_id})
                if code and imei_name and num_months:
                    self.env['aws.device.suscripcions'].create({'device_id':self.id,'code':str(code),'num_months':int(num_months)})
                    _logger.info(f'=== INSERT SUSCRIPCION '+str(code)+ ' TO DEVICE ' + str(imei_name))
                    lot = imei_id.imei_id
                    if lot:
                        if lot.life_date:
                            start_date = lot.life_date
                        else:
                            start_date = datetime.now()
                        # days_in_month = calendar.monthrange(start_date.year, start_date.month)[int(num_months)]
                        # new_date = start_date + timedelta(days=days_in_month)
                        new_date = start_date + relativedelta(months=num_months)
                        new_date = sync_datetime_zone(new_date.strftime("%d/%m/%Y %H:%M"))
                        lot.write({'life_date': new_date})
                        _logger.info(f'=== CHANGE LIFEDATE ' + new_date + ' TO DEVICE ' + str(imei_name))
                        return True
        return False

    #todo parece ser que se tiene que llamar en update_user o insert_user
    # device_id?? ellos no saben el id de odoo pero saben el imei
    def addLifeDate(self, device_id):
        device_id = self.browse(device_id)
        if device_id:
            if not device_id.partner_id:
                return False
            else:
                if device_id.suscripcions_ids:
                    num_months = 0
                    for suscripcion in device_id.suscripcions_ids:
                        num_months += suscripcion.num_months
                    if num_months>0:
                        lot = device_id.imei_id
                        if lot:
                            if lot.life_date:
                                start_date = lot.life_date
                            else:
                                start_date = datetime.now()
                            new_date = start_date + relativedelta(months=num_months)
                            new_date = sync_datetime_zone(new_date.strftime("%d/%m/%Y %H:%M"))
                            lot.write({'life_date': new_date})
                            _logger.info(f'=== CHANGE LIFEDATE ' + new_date + ' TO DEVICE ' + str(device_id.name))
                            return True
        return False

    # llamada externa por WS
    def getProductAndLifedate(self, imei_name):
        if imei_name:
            imei_id = self.search([('name','=',str(imei_name))])
            if imei_id:
                return {'product_code':imei_id.product_id.default_code if imei_id.product_id else None,'life_date':imei_id.imei_id.life_date.strftime('%Y-%m-%d') if imei_id.imei_id.life_date else None}
        return True


class AwsKey(models.Model):
    _name = 'aws.key'
    _description = 'AWS device key'

    keyPcbId = fields.Char('keyPcbId', required=True)
    name = fields.Char('name', related='macid')
    macid = fields.Char('MAC Id', related='mac_id.name')
    mac_id = fields.Many2one('stock.production.lot', string='MAC serial',
                              required=True)
    assembledOn = fields.Datetime(string='Assembled on', required=True)
    status = fields.Selection(SELECTION_FIELDS, 'Status', required=True)
#    testResult = fields.Char('testResult')
    ADC = fields.Selection(string='ADC', selection=SELECTION_FIELDS)
    FLASH = fields.Selection(string='FLASH', selection=SELECTION_FIELDS)
    ACCEL = fields.Selection(string='ACCEL', selection=SELECTION_FIELDS)
    INTR = fields.Selection(string='INTR', selection=SELECTION_FIELDS)
    CARGA = fields.Selection(string='CARGA', selection=SELECTION_FIELDS)
    BT = fields.Selection(string='BT', selection=SELECTION_FIELDS)
    scoreADC = fields.Integer('scoreADC')
    scoreFLASH = fields.Integer('scoreFLASH')
    scoreACCEL = fields.Integer('scoreACCEL')
    scoreINTR = fields.Integer('scoreINTR')
    scoreCARGA = fields.Integer('scoreCARGA')
    scoreBT = fields.Integer('scoreBT')
    OFF = fields.Selection(string='OFF', selection=SELECTION_FIELDS)
    scoreOFF = fields.Integer('scoreOFF')
    totalScore = fields.Integer('totalScore')
    
    def get_key_id_by_macid(self, macid):
        """Returns the device id matching imei's value"""
        return self.search([('macid', '=', macid)], limit=1)

    def insert_key(self):
        """Insert device's key. TODO: describe params"""
        obj_lot = self.env['stock.production.lot']
        result = []
        data = []
        for record in self.ids:
            macid = record.get('macid')
            if not self.get_key_id_by_macid(macid):
                record.update(record.pop('testResult'))
                on_date = record.pop('assembledOn')
                if on_date: record['assembledOn'] = sync_datetime_zone(on_date)
                record = obj_lot._add_serial_number(record, False)
                data.append(record)
        #======================================================================
        # data = [record for record in self.ids
        #         if not self.get_key_id_by_macid(record.get('macid'))]
        #======================================================================
        if self and not len(data): return True
        _logger.info(f'=== INSERT KEY: {data}')
        if data:
            try:
                result = self.create(data)
                for key in result: key.mac_id.write({'key_id': key.id})
                _logger.info(f'=== INSERT KEY: DONE')
            except Exception as e:
                _logger.info(f'=== INSERT KEY: FAIL')
                _logger.info(str(e))
                print(str(e))
                raise e
        return len(result) and result.ids or -1


class AwsDeviceIccid(models.Model):
    _name = 'aws.device.iccid'
    _description = 'AWS Device ICCID'

    name = fields.Char('ICCID')
    device_id = fields.Many2one('aws.device', 'Device')


class AwsFirmware(models.Model):
    _name = 'aws.firmware'
    _description = 'AWS Firmware'
    _rec_name = 'fwVersion'

    name1 = fields.Char('Firmware')
    fwVersion = fields.Char('Version')
    mtype = fields.Char('mtype')
    device_id = fields.One2many(
        comodel_name='aws.device',
        inverse_name='firmware_id',
        string='Device'
    )
    fwType = fields.Char('fwType')

    def insert_firmware(self):
        obj_device = self.env['aws.device']
        result = []
        data = []
        for record in self.ids:
            fw_id = self.search([('fwVersion', '=', record.get('fwVersion'))],
                                limit=1)
            device_id = obj_device.get_device_id_by_imei(record.get('imei'))
            if not fw_id:
                record.update({'name': record.pop('imei'),
                               'device_id': [(4, device_id.id, False)]})
                data.append(record)
            else: device_id and device_id.write({'firmware_id': fw_id.id})
        if self and not len(data): return True
        _logger.info(f'=== INSERT FIRMWARE: {data}')
        if data:
            try:
                result = self.create(data)
                device_id.write({'state': 'programmed'})
                _logger.info(f'=== INSERT FIRMWARE: DONE')
            except Exception as e:
                _logger.info(f'=== INSERT FIRMWARE: FAIL')
                _logger.info(str(e))
                print(str(e))
                raise e
        return len(result) and result.ids or -1


class AwsBrand(models.Model):
    _name = 'aws.brand'
    _description = 'AWS Brand'

    name = fields.Char('Brand')


class AwsModel(models.Model):
    _name = 'aws.model'
    _description = 'AWS Model'

    name = fields.Char('Model')


class AwsDeviceHistory(models.Model):
    _name = 'aws.device.history'
    _description = 'AWS Device History'
    #_rec_name = 'imei'

    device_id = fields.Many2one('aws.device', string='Device')
    #imei = fields.Char('IMEI')
    name = fields.Char('name', related='device_id.name')
    lastConnection = fields.Datetime('Last connection')

    def insert_history(self):
        """Insert device history, to register last connection."""
        device_obj = self.env['aws.device']
        res_data = []
        result = []
        data = self and self.ids
        _logger.info(f'=== INSERT HISTORY: {data}')
        for connection in data:
            imei = connection.pop('imei')
            l_date = connection.get('lastConnection')
            if l_date:
                connection['lastConnection'] = sync_datetime_zone(l_date)
                device_id = device_obj.get_device_id_by_imei(imei)
            if device_id:
                connection.update({'device_id': device_id.id})
                res_data.append(connection)
        if res_data:
            try:
                result = self.create(res_data)
                _logger.info(f'=== INSERT HISTORY: DONE')
            except Exception as e:
                _logger.info(f'=== INSERT HISTORY: FAIL')
                _logger.info(str(e))
                print(str(e))
                raise e
        return len(result) and result.ids or -1


class AwsDeviceTest(models.Model):
    _name = 'aws.device.test'
    _description = 'AWS Device Test'
    _rec_name = 'imei'

    imei = fields.Char('IMEI')
    device_id = fields.Many2one('aws.device', string='Device')
    name = fields.Char('name', related='device_id.name')
    testedOn = fields.Datetime('Tested on')
    testCaseId = fields.Char('Test Case Id')
    iccid = fields.Selection(string='ICCid', selection=SELECTION_FIELDS)
    GPRS = fields.Selection(string='GPRS', selection=SELECTION_FIELDS)
    FTPS = fields.Selection(string='FTPS', selection=SELECTION_FIELDS)
    GPS = fields.Selection(string='GPS', selection=SELECTION_FIELDS)
    IMU = fields.Selection(string='IMU', selection=SELECTION_FIELDS)
    memory = fields.Selection(string='Memory', selection=SELECTION_FIELDS)
    battery = fields.Selection(string='Battery', selection=SELECTION_FIELDS)
    status = fields.Selection(SELECTION_FIELDS, 'Status', required=True)
    scoreGPRS = fields.Integer('scoreGPRS')
    scoreFTPS = fields.Integer('scoreFTPS')
    scoreGPS = fields.Integer('scoreGPS')
    scoreIMU = fields.Integer('scoreIMU')
    iccidScore = fields.Integer('scoreICCid')
    scoreMemory = fields.Integer('scoreMemory')
    scoreBattery = fields.Integer('scoreBattery')
    totalScore = fields.Integer('totalScore')

    def is_passed_test(self):
        '''Check if all test have passed (OK)'''
        if self.GPRS == 'OK' and self.GPS == 'OK' and self.IMU == 'OK' and \
                self.memory == 'OK' and self.battery == 'OK' and self.iccid == 'OK':
            return True
        return False

    def insert_device_test(self):
        """Insert device test. This action it's known as 'Pruebas'."""
        device_obj = self.env['aws.device']
        res_data = []
        data = self and self.ids
        _logger.info(f'=== INSERT DEVICE TEST: {data}')
        for device_test in data:
            # TODO: if no 'imei' in device_test and device(s) with no imei !!!
            imei = device_test.pop('imei')
            results = device_test.pop('results')
            test_date = device_test.pop('testedOn')
            status = device_test.pop('status')
            if test_date:
                results['testedOn'] = sync_datetime_zone(test_date)
                device_id = device_obj.get_device_id_by_imei(imei)
                if not device_id:
                    msg0 = "Está tratando de insertar pruebas a un dispositivo"
                    msg1 = "con un número de IMEI [%s] que no se ha registrado"
                    raise UserError('%s%s' % (msg0, msg1 % imei))
                testCaseId = results.get('testCaseId')
                tc_args = [('testCaseId', '=', testCaseId),('imei', '=', imei)]
                rec_testCase = self.search(tc_args, limit=1)
                if not rec_testCase and results:
                    results.update({'device_id': device_id.id, 'imei': imei,
                                    'status': status})
                    res_data.append(results)
        if res_data:
            try:
                result = self.create(res_data)
                for res in result:
                    if res.is_passed_test():
                        res.device_id.write({'state': 'validated'})
                _logger.info(f'=== INSERT DEVICE TEST: DONE')
            except Exception as e:
                _logger.info(f'=== INSERT DEVICE TEST: FAIL')
                _logger.info(str(e))
                print(str(e))
                raise e
        else: return True
        return len(result) and result.ids or -1
