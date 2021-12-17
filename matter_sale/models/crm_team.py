from odoo import fields, models, api


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    @api.model
    def _default_warehouse_id(self):
        return self.env['sale.order']._default_warehouse_id()

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", required=True, default=_default_warehouse_id)
