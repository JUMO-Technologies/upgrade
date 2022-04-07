from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = "crm.lead"

    partner_category_ids = fields.Many2many("res.partner.category", string="Etiqueta")
