{
    'name': 'Auto Save Sales Orders',
    'version': '1.0.0',
    'category': 'Technical',
    'summary': 'Automatic saving of draft Sale Orders',
    'description': """
        Auto Save Sales Orders
        =======================
        
        Automatically saves draft records for:
        - Sale Orders (sale.order)
        
        Features:
        - Saves when a customer is first entered to create a valid record
        - Saves after 4 minutes of first creating the record
        - Then saves every 4 minutes if changes detected
        - Only saves when all required fields are filled
        - Only operates on draft state records
        - Prevents data loss from unsaved work
    """,
    'author': 'ProFast Supply Inc',
    'website': 'profast.supply',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'sale_management',
    ],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'auto_save_draft/static/src/js/auto_save_form_controller.js',
        ],
    },
    'images': ['static/description/banner(1).png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
