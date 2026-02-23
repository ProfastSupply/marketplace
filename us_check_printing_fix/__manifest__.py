# -*- coding: utf-8 -*-
{
    'name': 'US Check Printing - Address Fix',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations/Check',
    'summary': 'Adjusts check address position for US window envelopes',
    'description': """
US Check Printing — Address Fix for Odoo 18
============================================

Fixes the payee address position on printed US checks so it aligns correctly
with standard #10 window envelopes right out of the box. No configuration,
no label printing, no manual folding adjustments — install and print.

The Problem
-----------
Odoo's default US check layout (l10n_us_check_printing) positions the payee
address slightly off from the window cutout on a standard #10 business
envelope (4-1/8" x 9-1/2"). This causes the address to be partially or fully
hidden behind the envelope face when folded for mailing.

What This Module Fixes
----------------------

**#10 Window Envelope Alignment**
  Repositions the payee / vendor address block to show cleanly through the
  window of a standard #10 business envelope. Compatible with:
  - #10 window envelopes (standard US business envelope)
  - Double-window check envelopes
  - Preprinted check stock with address window
  - Top-stub, middle-stub, and bottom-stub check layouts

**Cleaner US Address Format**
  US addresses suppress the country line — no "United States" printed below
  the ZIP code. State prints as two-letter code (CA, TX, NY, FL) rather than
  full state name. International vendor addresses still include the country.

**Account Number Field & Memo Printing**
  Adds an Account Number field to vendor / partner records. When present,
  the account number prints automatically in the check memo line — useful
  for utility payments, loan payments, and vendor account references.

Compatibility
-------------
  Extends l10n_us_check_printing (Odoo's built-in US check module).
  Works with standard US letter paper (8.5" x 11").
  Compatible with blank check stock and preprinted MICR check paper.

Search Tags
-----------
US check printing | check address alignment | window envelope check |
#10 envelope | number 10 envelope | business envelope | check window |
payee address position | check layout fix | MICR check | check stock |
blank check stock | preprinted check | check paper | US letter check |
vendor check | accounts payable check | AP check printing |
check memo account number | vendor account number memo |
check address window | envelope window alignment | fold and mail check |
check mailing | USPS mailing | check format USA | American check format |
l10n_us check fix | US localization check | check printing address |
top stub check | bottom stub check | middle stub check | voucher check |
three-part check | checkbook printing | payroll check | vendor payment check |
double window envelope | check envelope | remittance check |
state abbreviation check | ZIP code check address | no country check address
    """,

    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'support': 'it@profast.supply',
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
