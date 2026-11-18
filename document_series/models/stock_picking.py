from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    series_id = fields.Many2one(
        'document.series', string='Serie', copy=False,
        domain="[('model_name', '=', 'stock.picking'),"
               " ('company_id', '=', company_id)]",
    )

    def button_validate(self):
        # Reemplaza el nombre por el correlativo de la serie al validar
        for picking in self.filtered(
                lambda p: p.series_id and p.state != 'done'
                and not p.name.startswith(f'{p.series_id.name}-')):
            picking.name = picking.series_id.get_next_number()
        return super().button_validate()
