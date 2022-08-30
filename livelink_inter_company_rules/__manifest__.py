{
    'name': "Livelink - Inter Company Module for Sale/Purchase Orders, Invoices, Pickings",

    'summary': """Livelink - Intercompany SO/PO/INV/Pick rules""",

    'description': """Intercompany SO/PO/INV/Pick rules""",

    'author': "TiOdoo",
    'website': "www.tiodoo.es",

    'category': 'Productivity',
    'version': '1.0',

    'depends': ['inter_company_rules'],

    'data': [
        'security/ir.model.access.csv',

        'views/intercompany_serials_view.xml',
        'views/res_company_view.xml',
        'views/stock_picking_view.xml',

    ],
    'installable': True,

}
