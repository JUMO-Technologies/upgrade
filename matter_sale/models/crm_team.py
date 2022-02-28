from odoo import fields, models, api


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    @api.model
    def _default_warehouse_id(self):
        return self.env['sale.order']._default_warehouse_id()

    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", required=True, default=_default_warehouse_id)
    assign_address = fields.Boolean('Assign Address')
    address = fields.Char('Address')
    cp = fields.Char('CP')
    email = fields.Char('Email')
    website = fields.Char('Website')
    logo = fields.Binary('Logo')
    phone = fields.Char('Phone')