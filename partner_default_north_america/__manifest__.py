# -*- coding: utf-8 -*-
{
    'name': 'Contact Default Country - North America',
    'version': '18.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Default partner country to US, limit selection to US/Canada/Mexico',
    'description': """
Partner Default Country - North America
=======================================

Sets United States as the default country for contacts and limits
country selection to US, Canada, and Mexico.

Features
--------
* Country field defaults to United States
* Country dropdown shows only US, Canada, Mexico
* State field shows states/provinces for selected country
* Reduces data entry errors for North American companies
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
