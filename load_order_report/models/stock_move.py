from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    purchase_origin = fields.Char(string="PO", compute="_compute_purchase_origin")

    @api.depends("move_orig_ids.picking_id.purchase_id")
    def _compute_purchase_origin(self):
        for move in self:
            move.purchase_origin = ",".join(move.move_orig_ids.mapped("picking_id.purchase_id.name"))
