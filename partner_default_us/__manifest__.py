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

Search Tags
-----------
default country United States | US only contacts | American contacts default |
limit country selection | restrict country field | US states only | domestic only contacts |
partner country default USA | contact country USA | res.partner default country |
United States default | force country US | American company contacts |
domestic partner setup | US localization contacts | state dropdown US only |
hide international states | remove country field | simplify contact form |
US address form | American address | partner form USA | contact data entry US |
CRM US only | customer default country | vendor default country US |
partner country restriction | single country Odoo | USA only Odoo |
contact form simplification | reduce data entry | domestic customers US |
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'support': 'it@profast.supply',
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
