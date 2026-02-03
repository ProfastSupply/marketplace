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
    """,
    'author': 'ProFast Supply',
    'website': 'https://profast.supply',
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
