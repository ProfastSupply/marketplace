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
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'license': 'LGPL-3',
    'depends': ['account', 'sale'],
    'data': [
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
