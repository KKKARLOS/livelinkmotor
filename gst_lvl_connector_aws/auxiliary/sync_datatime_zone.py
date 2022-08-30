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

from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from datetime import datetime
from pytz import timezone


def sync_datetime_zone(m_date):
    """Syncs datetime input with odoo datetime fields"""
    new_timezone = timezone("UTC")
    old_timezone = timezone("Europe/Madrid")
    if m_date:
        dt_planned = old_timezone.localize(
            datetime.strptime(str(m_date), "%d/%m/%Y %H:%M"))
        m_date = datetime.strftime(dt_planned.astimezone(new_timezone),
                                   DEFAULT_SERVER_DATETIME_FORMAT)
    return m_date
