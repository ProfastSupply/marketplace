{
    'name': 'No More Pennies – Sales Order Rounding',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': (
        'Auto-round sale order totals to 5¢, 25¢, or $1 — '
        'built for the post-penny era. Sales order rounding, '
        'cash rounding, penny elimination compliance.'
    ),
    'description': """
No More Pennies – Automatic Sales Order Rounding for Odoo 18
=============================================================

The U.S. is phasing out the penny. Cash transactions now need to round to the
nearest nickel — but your invoices still need to look professional and accurate.

This module handles it automatically, the right way.

HOW IT'S DIFFERENT FROM ODOO'S BUILT-IN CASH ROUNDING
------------------------------------------------------
Odoo's Cash Rounding adds a separate "rounding" line to the invoice.
This module adjusts unit prices directly across your order lines so the
final total is naturally clean — no extra line items, no awkward explanation
to customers, no rounding entries in your accounting.

WHAT IT DOES
------------
When you confirm a quotation, the module:

  1. Calculates the next rounded total (cents-5, cents-25, or $1 your choice)
  2. Back-calculates the exact pre-tax subtotal adjustment needed, using
     the actual tax rate of your order lines
  3. Distributes that adjustment evenly across all lines, updating
     each unit price proportionally by quantity
  4. Runs a correction pass to eliminate any residual caused by Odoo's
     per-line tax rounding so the final total is exactly right

MIXED TAX ORDERS
----------------
Orders that mix taxed and non-taxed lines (common in US sales) are handled
correctly. The adjustment targets only the dominant tax group, using that
group's actual tax rate no blended average, no guesswork.

SETTINGS  (Sales > Configuration > Settings > Total Rounding)
--------------------------------------------------------------
  Rounding Increment:  5 cents (default) / 25 cents / $1.00
  Round Up Only:       Always round to the NEXT increment, never down
                       (default: ON you never accidentally reduce a total)

UNLOCK and RE-CONFIRM SAFE
--------------------------
If you unlock a confirmed order to make edits, original unit prices are
restored automatically. Re-confirming applies rounding fresh to the
updated prices no stacking, no drift.

KEYWORDS
--------
sales order rounding, cash rounding odoo, penny elimination, no pennies,
nickel rounding, round to nearest 5 cents, round up total, price rounding,
US penny phase-out, automatic rounding odoo 18
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
