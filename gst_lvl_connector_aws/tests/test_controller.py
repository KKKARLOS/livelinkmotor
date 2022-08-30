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

from odoo import http
from werkzeug.utils import redirect
from ..controllers.aws_controllers import AwsControllers as controller


class TestControllers(http.Controller):

    @http.route('/test_insert_device', type='http', auth='public', crf=True)
    def test_controller_insert_device(self):
        redirect('/insert_device')
        # request.params['data'] = self.json_device_data()
        # request.redirect('/insert_device')

        #controller.controller_insert_device(self.json_device_data())

    @http.route('/test_insert_device_test', type='http', auth='public', crf=True)
    def test_controller_insert_device_test(self):
        controller.controller_insert_device_test(self.json_device_test())

    @http.route('/test_insert_firmware', type='http', auth='public', crf=True)
    def test_controller_insert_firmware(self):
        controller.controller_insert_firmware(self.json_insert_firmware())

    @http.route('/test_insert_user', type='http', auth='public', crf=True)
    def test_controller_insert_user(self):
        controller.controller_insert_user(self.json_insert_user())

    @http.route('/test_update_user', type='http', auth='public', crf=True)
    def test_controller_update_user(self):
        controller.controller_update_user(self.json_update_user())

    @http.route('/test_insert_history', type='http', auth='public', crf=True)
    def test_controller_insert_history(self):
        controller.controller_insert_history(self.json_insert_history())

    def json_device_data(self):
        return {
            "data":[{
                "imei": "XXXXXXXXXXXXXXX",
                "iccid": "YYYYYYYYYYYYYYY",
                "assembledOn": "01/04/2020 11:25",
                "status": "OK"
            },
                {"imei": "XXXXXXXXXXXXXXX",
                 "iccid": "YYYYYYYYYYYYYYY",
                 "assembledOn": "01/04/2020 11:26",
                 "status": "NOK"
                 },
            ]
        }

    def json_device_test(self):
        return {
            "data":[{
                "imei": "XXXXXXXXXXXXXXX",
                "iccid": "YYYYYYYYYYYYYYY",
                "testedOn": "01/04/2020 20:59",
                "status": "OK",
                "results":{
                    "testCaseId": 1234123213,
                    "GPRS": "OK",
                    "GPS": "OK",
                    "IMU": "OK",
                    "memory": "OK",
                    "battery": "OK"
                }
            },
            {
                "imei": "XXXXXXXXXXXXXXX",
                "iccid": "YYYYYYYYYYYYYYY",
                "testedOn": "01/04/2020 20:59",
                "status": "NOK",
                "results":{
                    "testCaseId": 1234123213,
                    "GPRS": "OK",
                    "GPS": "OK",
                    "IMU": "OK",
                    "memory": "OK",
                    "battery": "OK"
                }
            }]
        }

    def json_insert_firmware(self):
        return {
            "imei": "XXXXXXXXXXXXXXX",
            "fwVersion": "XX.XX",
            "mtype": "PP",
        }

    def json_insert_user(self):
        return {
            "data": [{
                    "imei": "XXXXXXXXXXXXXXX",
                    "userId": "aaaaa@bbbbbb.com"
                },
                {
                    "imei": "XXXXXXXXXXXXXXX",
                    "userId": "aaaaa2@bbbbbb.com"
                }]
            }

    def json_update_user(self):
        return {
            "data": [{
                    "imei": "XXXXXXXXXXXXXXX",
                    "brand": "Kawazaki",
                    "model": "ZXR 750",
                    "type":"Racing",
                    "currentKM":15001
                },
                {
                    "imei": "XXXXXXXXXXXXXXX",
                    "brand": "BWM",
                    "model": "K 1200 GT",
                    "type":"Racing",
                    "currentKM":18001
                }]
            }

    def json_insert_history(self):
        return {
            "data":[{
                "imei": "XXXXXXXXXXXXXXX",
                "lastConnection": "01/04/2020 17:56"
                },
                {
                    "imei": "XXXXXXXXXXXXXXX",
                    "lastConnection": "28/03/2020 10:27"
                }]
            }
