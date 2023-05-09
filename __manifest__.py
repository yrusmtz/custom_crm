# -*- coding: utf-8 -*-
{
    'name': "custom_crm",

    'summary': """
        Módulo CRM para la gestión de visitas""",

    'description': """
        Módulo CRM para la gestión de visitas...
    """,

    'author': "sury",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        #SEGURIDAD
        'security/security.xml',
        'security/ir.model.access.csv',
        
        #VISTAS
        'views/views.xml',
        'views/cliente.xml',
        'views/auto.xml',
        'views/taller.xml',
        'views/templates.xml',
    

        #REPORTES
        'reports/visit.xml',
        #'report/custom_crm_report_templates.xml',
    ],
    # only loaded in demonstration mode


    'demo': [
        'demo/demo.xml',
        ]
}
