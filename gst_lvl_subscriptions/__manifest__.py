# -*- coding: utf-8 -*-
{
    'name': "GST lvl subscriptions",
    'author': "RIIK - Innovación Gestión y Conocimiento S.L.",
    'website': "http://www.riik.es",
    'category': '',
    'version': '1.1',
    'depends': ['base', 'gst_lvl_connector_aws'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/services_line_views.xml',
        'views/history_views.xml'
    ],
    'installable': True,
    'auto_install': False,
}
