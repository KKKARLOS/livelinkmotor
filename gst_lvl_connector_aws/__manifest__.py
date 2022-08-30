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
{
    'name': "gst_lvl_connector_aws",

    'summary': """Connector AWS for Livelink""",

    'description': """Connector AWS for Livelink to gather devices's data""",

    'author': "Guadaltech Soluciones Tecnológicas S.L.",
    'website': "www.guadaltech.es",

    'category': 'Technical Settings',
    'version': '1.0',

    'depends': ['l10n_es', 'purchase_mrp', 'delivery', 'product_expiry'],

    'data': [
        'security/connector_asw_security.xml',
        'security/ir.model.access.csv',
        
        'data/product_data.xml',
        
        'views/device_views.xml',
        'views/key_views.xml',
        'views/device_test_views.xml',
        'views/firmware_views.xml',
        'views/history_views.xml',
        'views/partner_views.xml',
        'views/menu.xml',
        'views/mrp_view.xml',
        #======================================================================
        # 'views/product_template_view.xml',
        #======================================================================
        'views/stock_product_location.xml',
    ],

    'external_dependencies': {
        'python': ['pytz'],
    },
}
