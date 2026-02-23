# -*- coding: utf-8 -*-
{
    'name': 'Transfer & Invoice Improvements',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Delivery',

    'summary': (
        'Improved Navigation and Cut Down Clicks'
    ),

    'description': """
Transfer & Invoice Improvements for Odoo 18
============================================

Streamlines the delivery-to-invoice workflow by adding missing shortcuts
and quality-of-life features to stock transfers and draft invoices.

Key Features
------------

**Create Invoice Directly from Delivery**
  Create a customer invoice without leaving the delivery order (stock picking).
  Works on validated outgoing deliveries, drop shipments, and pick-pack-ship
  workflows. No need to navigate back to the sale order.

**Sales Order & Purchase Order Links on Transfers**
  Every transfer (delivery, receipt, return, internal) shows a clickable link
  to its originating sales order or purchase order — stock picking to SO/PO
  in one click.

**Regenerate Invoice Lines**
  Made changes to a delivery after invoicing? Click "Regenerate Lines" on any
  draft invoice to rebuild it from current delivered quantities. Handles
  partial deliveries, backorders, and quantity corrections automatically.

**Consolidate Draft Invoices**
  Multiple draft invoices for the same order are merged into one automatically
  when regenerating lines — keeping your accounting clean.

**Auto Invoice / Credit Note Switching**
  If the rebuilt total is negative (e.g. a return), the document type switches
  to credit note automatically.

**Improved Return Slip**
  Return delivery slips print "Return of [original delivery]" instead of the
  generic order reference.

Search Tags
-----------
delivery invoice | create invoice from transfer | stock picking invoice |
pick ticket | pick slip | delivery slip | receiving | goods receipt |
warehouse transfer | outgoing shipment | incoming receipt | backorder invoice |
regenerate invoice lines | rebuild invoice | consolidate invoices |
sale order delivery | purchase order receipt | invoice from warehouse |
delivery order workflow | picking list | packing slip | shipping invoice |
WMS invoice | fulfillment invoice | dispatch invoice | transfer invoice |
stock move invoice | validated delivery invoice | delivery to invoice |
invoice from picking | one-click invoice | delivery invoice button
    """,

    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'support': 'it@profast.supply',
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
