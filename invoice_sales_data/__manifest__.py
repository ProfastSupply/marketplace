# -*- coding: utf-8 -*-
{
    'name': 'Invoice Sales Data',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Track cost, revenue, and profit on customer invoices',
    'description': """
Invoice Sales Data
==================
Adds cost and profit tracking to customer invoices and partners:

**Invoice Level:**
* **Cost**: Automatically calculated from product standard costs on invoice lines
* **Profit**: Revenue minus cost, visible on invoices and list views
* **Real-time**: Updates automatically when invoice lines change (within 7 days)
* **Historical freeze**: Values lock after 7 days to preserve accuracy when product costs change

**Partner Level:**
* **Total Profit**: Lifetime profit from all invoices and credit notes
* **Avg Profit Per Sale**: Average profit per invoice (excludes credits from average)
* **Sales Count**: Number of posted invoices for this customer

**Admin-only**: All fields visible only to Billing Administrators
**No manual intervention**: Fully automatic
**One-time compute**: All historical invoices compute on module install

Applies to customer invoices (out_invoice) and credit notes (out_refund).

Search Tags
-----------
invoice profit | invoice cost | invoice margin | profit on invoice |
cost tracking invoice | revenue cost profit Odoo | invoice profitability |
customer invoice profit | profit per invoice | margin per invoice |
invoice gross profit | invoice net profit | sales margin invoice |
product cost invoice | standard cost invoice | COGS invoice |
cost of goods sold invoice | invoice cost analysis | profit analysis invoice |
customer profitability | partner profit | lifetime customer profit |
customer lifetime value | customer LTV Odoo | partner lifetime profit |
avg profit per sale | average profit customer | customer profit tracking |
most profitable customers | customer revenue analysis | partner sales analytics |
invoice profit visibility | billing admin profit | admin only margin |
profit margin hidden | sensitive margin data | margin visibility control |
historical invoice profit | freeze invoice cost | invoice cost lock |
7 day freeze | cost change protection | historical cost freeze |
invoice profit column | profit list view | invoice profit total |
bulk invoice compute | post install hook profit | invoice analytics Odoo |
account.move profit | account move cost | invoice margin field |
out_invoice profit | credit note profit | profit tracking accounting |
real time invoice profit | automatic profit calculation | invoice cost auto |
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'support': 'it@profast.supply',
    'license': 'LGPL-3',
    'depends': ['account', 'sale'],
    'data': [
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
