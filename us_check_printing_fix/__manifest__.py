# -*- coding: utf-8 -*-
{
    'name': 'US Check Printing - Address Fix',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations/Check',
    'summary': 'Adjusts check address position for US window envelopes',
    'description': """
US Check Printing - Address Fix
===============================

Fixes the address position on printed checks to align correctly with standard US window envelopes.

Features
--------
* Repositions the payee address to align with envelope windows
* Adds Account Number field to partner records
* Prints Account Number in the check memo area
* Hides country name for US addresses (cleaner formatting)

Usage
-----
1. Install this module
2. Optionally add Account Numbers to your vendors
3. Print checks as normal - address will now align with window envelopes
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'l10n_us_check_printing',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/report_check.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
