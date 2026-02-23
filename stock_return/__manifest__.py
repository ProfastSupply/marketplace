# -*- coding: utf-8 -*-
{
    'name': 'Stock Return Max Quantities',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'One-click return all delivered quantities',
    'description': """
Stock Return Max Quantities
===========================
Adds a "Return Max Quantities" button to the return wizard that:
1. Sets all line quantities to their maximum (delivered qty)
2. Processes the return immediately

Saves time when returning entire deliveries.

Search Tags
-----------
stock return max quantity | return all quantities | one click return |
return full delivery | return entire order | stock return wizard |
return max button | return picking wizard | bulk return stock |
return all items | full return delivery | return delivered quantities |
stock picking return | return transfer | reverse delivery |
return shipment | return all lines | set max return qty |
return wizard button | stock return improvement | return picking max |
inventory return | warehouse return | full stock return |
return delivery order | return goods | RMA return merchandise |
return merchandise authorization | customer return | vendor return |
goods return | return to supplier | return to vendor |
reverse transfer | undo delivery | reverse shipment |
stock.return.picking | return picking view | return wizard Odoo |
one click reverse | return entire shipment | max qty return | receiving | recieving
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
    'support': 'it@profast.supply',
    'license': 'LGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_return_picking_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
