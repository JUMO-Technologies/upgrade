from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    team_warehouse_id = fields.Many2one(related="team_id.warehouse_id", string="Team Warehouse")
    warehouse_id = fields.Many2one(domain="[('id', '=', team_warehouse_id)]")

    @api.onchange('team_id')
    def _onchange_team_warehouse(self):
        domain = [('id', '=', self.team_id and self.team_id.warehouse_id.id or 0)]
        warehouse = self.warehouse_id.filtered_domain(domain)
        if not warehouse and self.team_id:
            warehouse = self.team_id.warehouse_id
        return {
            'domain': {'warehouse_id': domain},
            'value': {'warehouse_id': warehouse}
        }

    @api.constrains('warehouse_id')
    def _constrains_warehouse_team(self):
        for sale in self:
            if sale.state in ['draft', 'sent'] and sale.team_id and sale.warehouse_id and \
                    sale.warehouse_id.id != sale.team_id.warehouse_id.id:
                raise ValidationError(_("The chosen warehouse is not available to this sales team."))
