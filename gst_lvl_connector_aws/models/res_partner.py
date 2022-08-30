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

import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    device_ids = fields.One2many(
        comodel_name='aws.device',
        inverse_name='partner_id',
        string='Device'
    )
    brand = fields.Many2one('aws.brand', string='Brand')
    model = fields.Many2one('aws.model', string='Model')
    type_model = fields.Char(string='Model type')
    currentKM = fields.Char(string='currentKM')

    def get_partner_id_by_imei(self, imei):
        """Returns partner_id matching the imei's value"""
        return self.search([('imei', '=', imei)], limit=1)

    def insert_user(self):
        """Insert user. This action it's known as 'Setup'."""
        res_data = []
        result = []
        device_obj = self.env['aws.device']
        data = self and self.ids
        _logger.info(f'=== INSERT USER: {data}')
        for user in data:
            # TODO: if no 'imei' in device_test and device(s) with no imei !!!
            imei = user.pop('imei')
            device_id = device_obj.get_device_id_by_imei(imei)
            if device_id:
                userid = user.pop('userId')
                user.update({
                    'device_ids': [(4, device_id.id, False)],
                    'ref': userid,
                    'name': userid,
                    'email': userid,
                })
                res_data.append(user)
            else: raise UserError("No existe el dispositivo (IMEI: %s)" % imei)
        if res_data:
            try:
                result = self.create(res_data)
                device_id.write({'state': 'registered'})
                _logger.info(f'=== INSERT USER: DONE')
            except Exception as e:
                _logger.info(f'=== INSERT DEVICE: FAIL')
                _logger.info(str(e))
                print(str(e))
                raise e
        return len(result) and result.ids or -1

    def update_user(self):
        """Update user information with extra info."""
        result = []
        brand_obj = self.env['aws.brand']
        model_obj = self.env['aws.model']
        data = self and self.ids
        _logger.info(f'=== INSERT USER: {data}')
        for dicc_partner in data:
            try:
                # TODO: if no 'imei' in device_test and device(s) with no imei !!!
                imei = dicc_partner.pop('imei')
                device_id = self.env['aws.device'].get_device_id_by_imei(imei)
                if device_id and device_id.partner_id:
                    partner = device_id.partner_id
                    # update partner
                    brand = dicc_partner.pop('brand')
                    if brand:
                        bargs = [('name', 'like', brand)]
                        rec_brand = brand_obj.search(bargs, limit=1)
                        if not rec_brand:
                            rec_brand = brand_obj.create({'name': brand})
                        dicc_partner['brand'] = rec_brand.id
                    model = dicc_partner.pop('model')
                    if model:
                        margs = [('name', 'like', model)]
                        rec_model = model_obj.search(margs, limit=1)
                        if rec_model:
                            dicc_partner['model'] = rec_model.id
                        else:
                            rec_model = model_obj.create({'name': model})
                        dicc_partner['model'] = rec_model.id
                    type_model = dicc_partner.pop('type')
                    if type_model: dicc_partner['type_model'] = type_model
                    partner.write(dicc_partner)
                    result.append(partner.id)
                elif not device_id:
                    raise UserError("No existe el dispositivo (IMEI: %s)"% imei)
                else:
                    msg = "El dispositivo (IMEI: %s) no tiene cliente asociado"
                    raise UserError(msg % imei)
            except Exception as e:
                _logger.info(f'=== INSERT DEVICE: FAIL')
                _logger.info(str(e))
                print(str(e))
                raise e
        return len(result) and result or -1
