# -*- coding: utf-8 -*-
{
    'name': "custom_crm",

    'summary': """
        Módulo CRM para la gestión de visitas""",

    'description': """
        Módulo CRM para la gestión de visitas...
    """,

    'author': "curso odoo",
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
        'security/ir.model.access.csv',
        
        #VISTAS
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
   
}