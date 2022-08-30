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


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_invoice_sent(self):
        """Overrides this method contexts to pop custom_layout from dict."""
        res = super(AccountMove, self).action_invoice_sent()
        context = res.get('context', False)
        if context:
            context.pop('custom_layout', False)
        return res
