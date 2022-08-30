# -*- coding: utf-8 -*-
{
    'name': "GST LVL Odoo Studio Old Customizations",

    'summary': """
        Old customizations
        """,
    'description': """
        Odoo customizations from Odoo Studio are packaged in this module.
    """,

    'author': "Guadaltech",

    'category': 'Uncategorized',
    'version': '13.0.0.1.0',

    'depends': [
        'sale_stock',
        'stock',
        'purchase',
        'hr',
        'mrp',
        'woo_commerce_ept',
        'gst_lvl_reports',  # [ADD] related field to product_lot 
    ],

    'data': [
        'views/studio_custom_views.xml',
    ],
}
