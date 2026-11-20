from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    series_id = fields.Many2one(
        'document.series', string='Serie', copy=False, tracking=True,
        domain="[('model_name', '=', 'account.move'),"
               " ('company_id', '=', company_id),"
               " ('journal_id', 'in', (journal_id, False)),"
               " '|', ('l10n_latam_document_type_id', '=', l10n_latam_document_type_id),"
               " ('l10n_latam_document_type_id', '=', False)]",
    )

    @api.onchange('journal_id', 'l10n_latam_document_type_id')
    def _onchange_journal_series(self):
        if not self.journal_id or not self.is_sale_document(include_receipts=True):
            return
        if self.l10n_latam_use_documents and not self.l10n_latam_document_type_id:
            self.series_id = False
            return
        Series = self.env['document.series']
        domain = [
            ('model_name', '=', 'account.move'),
            ('company_id', '=', self.company_id.id),
        ]
        if self.l10n_latam_document_type_id:
            domain.append(
                ('l10n_latam_document_type_id', '=', self.l10n_latam_document_type_id.id))
        self.series_id = (
            Series.search(domain + [('journal_id', '=', self.journal_id.id)], limit=1)
            or Series.search(domain + [('journal_id', '=', False)], limit=1)
        )

    def _post(self, soft=True):
        # El nombre se escribe completo (ej. B001-00000002) y NO se usa el
        # prefijo del tipo de documento, para evitar "False B001-..." o "B B001-...".
        for move in self.filtered(
                lambda m: m.series_id and m.state == 'draft'
                and m.is_sale_document(include_receipts=True)
                and m.name in (False, '/', 'New')):
            move.name = move.series_id.get_next_number()
        return super()._post(soft=soft)
