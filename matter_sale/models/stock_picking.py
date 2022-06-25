from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_stock_old = fields.Boolean(string="In stock for 15 days", compute="_compute_is_stock_old", store=True)
    delivered = fields.Boolean(string="Delivered")

    @api.depends("group_id")
    def _compute_is_stock_old(self):
        days15date = fields.Datetime.subtract(fields.Datetime.now(), days=15)
        for product in self:
            product.is_stock_old = product._get_is_stock_old(days15date)

    def _get_is_stock_old(self, days15date):
        self.ensure_one()
        if self.picking_type_id.code == 'incoming' and self.state == 'done' and self.group_id:
            picking = self.search([('group_id', '=', self.group_id.id),
                                   ('picking_type_id.code', '=', 'outgoing'),
                                   ('date_done', '>=', self.date_done), ('state', '!=', 'cancel')],
                                  order="date_done asc", limit=1)
            if self.date_done <= days15date and picking.state != 'done':
                return True
        return False
