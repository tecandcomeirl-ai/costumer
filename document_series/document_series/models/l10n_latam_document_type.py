from odoo import fields, models


class L10nLatamDocumentType(models.Model):
    _inherit = 'l10n_latam.document.type'

    series_ids = fields.One2many(
        'document.series', 'l10n_latam_document_type_id', string='Series')
