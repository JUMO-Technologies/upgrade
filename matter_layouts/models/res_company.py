from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fiscal_name = fields.Char(string="Fiscal Name")


class ResCompany(models.Model):
    _inherit = 'res.company'

    fiscal_name = fields.Char(related="partner_id.fiscal_name", readonly=False)
