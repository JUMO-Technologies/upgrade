from odoo import models, fields, api


class PurchaseOrder(models.Model):
    """."""

    _inherit = "purchase.order"

    x_studio_field_Wj1eI = fields.Boolean()

    falta_confirmacion = fields.Boolean(string="Falta Confirmación de Fábrica")
