{
    'name': 'GST Livelink Stock',
    'version': '0.0.1',
    'author': 'Guadaltech S.L.',
    'license': 'GPL-3',
    'category': '',
    'depends': ['stock','gst_lvl_connector_aws'],
    'data': [
        'views/ir_sequence_views.xml',
        'views/product_product_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_production_lot_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
