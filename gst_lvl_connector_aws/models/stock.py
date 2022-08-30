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
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression



class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    device_id = fields.Many2one('aws.device', string='IMEI number')
    key_id = fields.Many2one('aws.key', string='MACID number')
    is_device = fields.Boolean(string='is Device?', default=False)
    is_mac = fields.Boolean(string='is Mac?', default=False)
    partner_id = fields.Many2one(related='device_id.partner_id')
    email = fields.Char(related='device_id.partner_id.email')

    @api.model
    def create(self,vals):
        return super(StockProductionLot,self).create(vals)

    def _get_company_by_email(self, vals):
        rec_user = self.env['res.users']
        if 'email' in vals:
            args = [('login', '=', vals.pop('email'))]
            rec_user = self.env['res.users'].search(args, limit=1)
        if rec_user: return rec_user.company_id.id
        else: return 2

    def _add_serial_number(self, vals, is_device):
        is_device = False
        if vals.get('imei'):
            ref = vals.get('imei')
            # pname = 'gst_lvl_connector_aws.product_product_device_imei'
            pname = 'gst_lvl_connector_aws.product_product_serial_imei'
            is_device = 'imei'
        if vals.get('macid'):
            ref = vals.get('macid')
            # pname = 'gst_lvl_connector_aws.product_product_device_macid'
            pname = 'gst_lvl_connector_aws.product_product_serial_macid'
            is_device = 'macid'
        product = self.env.ref(pname)
        cid = self._get_company_by_email(vals)
        lot_id = self._create_serial_number(ref, product, cid, is_device)
        if lot_id: self._update_qty_inventory(lot_id, product)

        if vals.get('imei'):
            vals.pop('imei')
            vals['imei_id'] = lot_id.id

        if vals.get('macid'):
            vals.pop('macid')
            vals['mac_id'] = lot_id.id

        return vals

    def _update_qty_inventory(self, lot_id, product, qty=1):
        args = [('company_id', '=', lot_id.company_id.id)]
        stock_wh = self.env['stock.warehouse'].search(args, limit=1)
        loc_id = self.env['stock.location'].browse(stock_wh.lot_stock_id.id)
        self.env['stock.quant']._update_available_quantity(
            product, loc_id, qty, lot_id
        )
        if qty < 1:
            self.env['stock.quant']._update_reserved_quantity(
                product, loc_id, 1, lot_id
            )

    def _create_serial_number(self, ref, product, company, who_is, isauto=False):
        try:
            # cid = self.env.ref('base.main_company').id
            # cid = self.env.user.company_id.id

            is_mac = True if who_is == 'macid' else False
            is_device = who_is == 'imei' and True or False

            return self.create({'name': ref, 'product_id': product.id,
                               'company_id': company, 'is_device': is_device,
                               'is_mac': is_mac, 'is_autogenerated': isauto})
        except Exception as e:
            raise UserError('Error con el serial %s' % ref)

    @api.model
    def search(self, args, **kwargs):
        args = expression.normalize_domain(args)
        _name = ''
        for arg in args:
            if isinstance(arg, (list, tuple)) and (arg[0] == "name"):
                # TODO: solo toma el primer nombre!! los OR en el search no van
                _name = arg[2]
                break
        if _name and type(_name) == type(''):
            _domain = [('devicePcbId', '=', _name)]
            devices = self.env['aws.device'].search(_domain)
            keys = self.env['aws.key'].search([('keyPcbId', '=', _name)])
            if devices:
                _domain = [('device_id', 'in', devices.ids)]
                args = expression.OR([args, _domain])
            if keys:
                args = expression.OR([args, [('key_id', 'in', keys.ids)]])
        return super(StockProductionLot, self).search(args, **kwargs)

    def _validate_test(self):
        is_ok = True
        imei_lot = False
        if self.key_id: imei_lot = self.key_id
        if self.device_id:
            imei_lot = self.device_id
        # ToDo: Aplicar a Keys cuando AWS esté preparado
            objTest = self.env['aws.device.test']   # Check Tests
            args = [('device_id', '=', self.device_id.id)]
            recTest = objTest.search(args, limit=1, order='id desc')
            if not recTest:
                raise UserError('Este IMEI [%s] no ha pasado los test de QA.' \
                            % imei_lot.name)
        if imei_lot and imei_lot.status != 'OK':
            raise UserError('Este IMEI [%s] tiene Bootstrapping "Not OK".' \
                            % imei_lot.name)
        return is_ok