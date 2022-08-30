# -*- coding: utf-8 -*-
{
    'name': "Gst lvl catalog",
    'version': '1.1',
    'author': "RIIK - Innovación Gestión y Conocimiento S.L.",
    'website': "http://www.riik.es",
    'category': '',
    'depends': ['base','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/subscriptionViews.xml',
        'views/catalogSubscriptionViews.xml',
        'views/subscriptionsTypeViews.xml',
        'views/subscriptionViewInProductInherit.xml',
        'views/servicesViews.xml'
    ],
    'installable': True,
    'auto_install': False,
}
