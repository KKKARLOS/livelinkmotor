{
    'name': 'GST Livelink Reports',
    'version': '3.0.1',
    'author': 'Guadaltech S.L.',
    'license': 'GPL-3',
    'category': '',
    'depends': [
        'stock',
    #    'report_batch',  Eliminada dependencia para desconectar OCA
        'account',
        'sale_management'
    ],
    'data': [
        'data/report_komobi_invoices_paperformat_data.xml',
        'reports/report_packaging_paperformat.xml',
        'reports/report_stock_packaging_and_qr.xml',
        'reports/report_stock_production_lot_paperformat.xml',
        'reports/report_packaging.xml',
        'reports/report_stock_production_lot.xml',
        'views/report_invoice.xml',
        'views/stock_views.xml',
        'views/product_view_inherit.xml',
        'data/mail_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
