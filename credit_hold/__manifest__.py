# -*- coding: utf-8 -*-
{
    'name': 'Customer Credit Hold',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Locks Sales Order Confirmation for Customers Over Transaction Limit',
    'description': """
Customer Credit Hold
=================================
Able to Set Amount for Individual Customers and a Restriction on Sales Orders will Trigger Once Unpaid Invoices Exceed Said Amount.
The Restriction Will be Automatically Removed Once the Customer's Account Falls Below the Limit.

Features
--------
* Set a Credit Limit on individual Customer records
* Accounts are automatically flagged On Hold when unpaid invoices exceed the limit
* Holds are automatically lifted when the balance falls back below the limit
* Sale Orders for customers on hold are blocked until an approver confirms them
* Configure the approver and activity recipient in Sales > Configuration > Settings

Search Tags
-----------
credit hold | customer credit limit | credit limit sales order | block order credit |
account on hold | credit risk management | customer credit control |
AR credit management | accounts receivable limit | credit check sales |
credit approval workflow | order approval credit | sales order block |
credit limit exceeded | overdue customer block | unpaid invoice limit |
credit controller | credit manager Odoo | customer balance limit |
automatic credit hold | credit hold approval | approve credit hold |
release credit hold | lift credit hold | credit hold notification |
sales order hold | order confirmation blocked | credit risk workflow |
customer payment hold | outstanding invoice limit | credit exposure limit |
accounts receivable hold | AR hold | credit terms enforcement |
customer risk management | bad debt prevention | credit policy enforcement |
credit hold approver | sales approval workflow | order blocked approval |
credit hold activity | credit management Odoo | customer creditworthiness |
prevent overselling | credit control module | customer debt limit |
invoice balance limit | per customer credit limit | individual credit limit |
automatic hold release | credit hold automation | scheduled credit check |
credit hold banner | credit hold warning | sales order warning credit |
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'support': 'it@profast.supply',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'contacts',
        'account',
        'sale_management',
        'mail',
        'web_studio',
        'base_automation',
    ],
    'data': [
        'data/credit_hold_approval_rule.xml',
        'data/credit_hold_automation.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
