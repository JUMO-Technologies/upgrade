from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_order_template_id = fields.Many2one('sale.order.template', string="Default Template")
