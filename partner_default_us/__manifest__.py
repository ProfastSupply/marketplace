# -*- coding: utf-8 -*-
{
    'name': 'Contact Default Country - US Only',
    'version': '18.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Default partner country to United States, limit state selection to US states',
    'description': """
Partner Default Country - US Only
=================================

Sets United States as the default country for contacts and limits
state/country selection to US only.

Features
--------
* Country field defaults to United States
* State field only shows US states
* Reduces data entry errors for US-based companies
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
