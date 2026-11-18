{
    'name': 'Series de documentos',
    'version': '19.0.1.1.1',
    'category': 'Accounting/Localizations',
    'summary': 'Series personalizadas (F001, B001, T001...) por tipo de documento',
    'depends': ['account', 'stock', 'l10n_latam_invoice_document'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/document_series_views.xml',
        'views/account_move_views.xml',
        'views/l10n_latam_document_type_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
