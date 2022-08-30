{
    'name': "RRHH Livelink",

    'summary': """Redefines standard Odoo HR behavior""",

    'description': """Redefines standard Odoo HR behavior""",

    'author': "TiOdoo",
    'website': "www.tiodoo.es",

    'category': 'Human Resources/Employees',
    'version': '1.0',

    'depends': ['hr_holidays', 'hr_contract'],

    'data': [

        'data/hr_leave_type_data.xml',
        'data/ir_cron.xml',

        'views/hr_attendance_view.xml',
        'views/hr_leave_view.xml',

    ],
    'installable': True,

}
