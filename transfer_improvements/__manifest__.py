# -*- coding: utf-8 -*-
{
    'name': 'Stock Picking & Invoice Improvements',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Delivery',
    'summary': 'Create Invoice from delivery, show SO/PO links, regenerate invoice lines',
    'description': """
Stock Picking & Invoice Improvements
====================================

Enhances delivery orders and invoices with useful workflow features.

Delivery Order Features
-----------------------
* Create Invoice button directly on outgoing deliveries
* Shows linked Sales Order (clickable)
* Shows linked Purchase Order for incoming transfers
* Improved return slip shows "Return of" instead of "Order"

Invoice Features
----------------
* Regenerate Invoice Lines button on draft invoices
* Rebuilds invoice from delivered quantities on the sale order
* Consolidates multiple draft invoices for the same order
* Auto-switches between invoice/credit note based on total

Usage
-----
1. For outgoing deliveries: Validate, then click "Create Invoice"
2. For invoices: Click "Regenerate Lines" to rebuild from deliveries
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'sale_stock',
        'purchase_stock',
        'account',
    ],
    'data': [
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
        'report/report_delivery_document.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
