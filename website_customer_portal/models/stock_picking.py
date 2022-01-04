from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    x_studio_field_bQQ6B = fields.Boolean()
