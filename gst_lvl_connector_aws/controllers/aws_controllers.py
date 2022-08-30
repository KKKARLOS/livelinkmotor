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
from odoo.http import request

import logging

_logger = logging.getLogger(__name__)
# TODO: decorator to add logs to all methods
# TODO: decorator to  check kw dict structure or missing arguments


class AwsControllers(http.Controller):

    @http.route('/insert_device', type='json', auth='public', crf=True)
    def controller_insert_device(self, **kw):
        request.env['aws.device'].insert_device(kw)

    @http.route('/insert_key', type='json', auth='public', crf=True)
    def controller_insert_key(self, **kw):
        request.env['aws.key'].insert_device(kw)

    @http.route('/insert_device_test', type='json', auth='public', crf=True)
    def controller_insert_device(self, **kw):
        request.env['aws.device.test'].insert_device_test(kw)

    @http.route('/insert_firmware', type='json', auth='public', crf=True)
    def controller_insert_firmware(self, **kw):
        request.env['aws.firmware'].insert_firmware(kw)

    @http.route('/insert_user', type='json', auth='public', crf=True)
    def controller_insert_user(self, **kw):
        request.env['res.partner'].insert_user(kw)

    @http.route('/update_user', type='json', auth='public', crf=True)
    def controller_update_user(self, **kw):
        request.env['res.user'].update_user(kw)

    @http.route('/insert_history', type='json', auth='public', crf=True)
    def controller_insert_history(self, **kw):
        request.env['aws.device.history'].insert_history(kw)
