# -*- coding: utf-8 -*-
{
    'name': 'Contact Default Country - North America',
    'version': '18.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Default partner country to United States, limit state selection to US, Canada, and Mexico',
    'description': """
Partner Default Country - North America
========================================
Sets United States as the default country for contacts and limits
state/country selection to North America (United States, Canada, Mexico).

Features
--------
* Country field defaults to United States
* Country dropdown limited to United States, Canada, and Mexico
* State field only shows states/provinces for US, Canada, and Mexico
* Reduces data entry errors for North America-based companies

Search Tags
-----------
default country North America | US Canada Mexico contacts | NAFTA contacts |
USMCA contacts | North American contacts | limit country selection |
restrict country to North America | US Canada Mexico only | domestic contacts North America |
partner country default USA Canada Mexico | contact country North America |
res.partner default country | United States Canada Mexico | force country North America |
North American company contacts | partner form North America | CRM North America |
customer default country | vendor default country North America |
partner country restriction | three country Odoo | USA Canada Mexico Odoo |
contact form simplification | reduce data entry | Canadian provinces | Mexican states |
US states Canadian provinces | hide international countries | domestic customers North America |
continental contacts | Americas contacts | North American localization |
partner setup North America | address form North America |
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
