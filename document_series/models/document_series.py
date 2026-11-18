from odoo import api, fields, models


class DocumentSeries(models.Model):
    _name = 'document.series'
    _description = 'Serie de documentos'
    _order = 'model_name, name'

    name = fields.Char('Serie', required=True, help='Ej.: F001, B001, T001')
    document_type = fields.Selection([
        ('invoice', 'Factura'),
        ('receipt', 'Boleta'),
        ('credit_note', 'Nota de crédito'),
        ('debit_note', 'Nota de débito'),
        ('delivery', 'Guía de remisión'),
        ('other', 'Otro'),
    ], string='Tipo de documento', required=True, default='invoice')
    l10n_latam_document_type_id = fields.Many2one(
        'l10n_latam.document.type', string='Tipo de documento (SUNAT)',
        index=True,
        help='Tipo del catálogo: 01 Factura, 03 Boleta, 07 Nota de crédito...')
    model_name = fields.Selection([
        ('account.move', 'Facturación'),
        ('stock.picking', 'Inventario'),
    ], string='Aplica a', required=True, default='account.move')
    journal_id = fields.Many2one(
        'account.journal', string='Diario',
        domain="[('company_id', '=', company_id)]")
    padding = fields.Integer('Longitud del correlativo', default=8)
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company)
    sequence_id = fields.Many2one(
        'ir.sequence', string='Secuencia', readonly=True, copy=False)
    next_number = fields.Integer(
        'Próximo número', compute='_compute_next_number',
        inverse='_inverse_next_number')
    active = fields.Boolean(default=True)

    _name_company_uniq = models.Constraint(
        'unique(name, model_name, company_id)',
        'La serie ya existe para este modelo y compañía.',
    )

    @api.depends('sequence_id.number_next_actual')
    def _compute_next_number(self):
        for rec in self:
            rec.next_number = rec.sequence_id.number_next_actual or 1

    def _inverse_next_number(self):
        for rec in self:
            if rec.sequence_id and rec.next_number > 0:
                rec.sequence_id.sudo().number_next_actual = rec.next_number

    def _prepare_sequence_vals(self):
        self.ensure_one()
        return {
            'name': f'Serie {self.name} ({self.model_name})',
            'code': f'document.series.{self.id}',
            'prefix': f'{self.name}-',
            'padding': self.padding,
            'company_id': self.company_id.id,
            'implementation': 'no_gap',
        }

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec.sequence_id = self.env['ir.sequence'].sudo().create(
                rec._prepare_sequence_vals())
        return records

    def write(self, vals):
        res = super().write(vals)
        if {'name', 'padding'} & set(vals):
            for rec in self.filtered('sequence_id'):
                rec.sequence_id.sudo().write({
                    'prefix': f'{rec.name}-',
                    'padding': rec.padding,
                })
        return res

    def unlink(self):
        sequences = self.sequence_id.sudo()
        res = super().unlink()
        sequences.unlink()
        return res

    def get_next_number(self):
        self.ensure_one()
        return self.sequence_id.sudo()._next()
