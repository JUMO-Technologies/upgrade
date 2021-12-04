from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_sale_order_template_id = fields.Many2one(related="company_id.sale_order_template_id", readonly=False)

    @api.model
    def _set_default_sale_order_template_id_if_empty(self):
        return
