{
    'name': "livelink_woo_subscription",

    'summary': """Redefines WooCommerce Odoo Apps""",

    'description': """Redefines WooCommerce Odoo Apps""",

    'author': "TiOdoo",
    'website': "www.tiodoo.es",

    'category': 'Sale',
    'version': '1.01',

    'depends': ['sale_subscription', 'woo_commerce_ept', 'gst_lvl_connector_aws'],

    'data': [

        'security/ir.model.access.csv',

        'wizard/locate_suscription_view.xml',

        'views/aws_subscription_view.xml',
        'views/sale_subscription_view.xml',

    ],
    'installable': True,

}
