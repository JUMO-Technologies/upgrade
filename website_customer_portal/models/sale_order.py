from odoo import models, fields, api
from itertools import groupby
import operator


STATES = [
    ("approved", "Presupuesto aprobado"),
    ("processed", "Pedido tramitado"),
    ("at warehouse", "Pedido en almacén"),
    ("delivered", "Pedido entregado"),
]


class SaleOrder(models.Model):
    """."""

    _inherit = "sale.order"

    x_studio_field_RBuAR = fields.Char()
    # The field above was added in with studio, there is need to re-defined it here

    x_opportunity_ids = fields.Char(string="ID de oportunidad", compute="_compute_x_opportunity_ids")
    count_opportunity_id = fields.Integer(string="Count Opportunity", compute="_compute_count_opportunity_id")
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Usuario Delivery")

    def opportunity_portal_url(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        """Get a portal url for opportunity model, including access_token.
      
        """
        base_path = "/my/%s/dashboard" % (self._name,)
        self.ensure_one()
        url = base_path + "%s?access_token=%s%s%s%s%s" % (
            suffix if suffix else "",
            self._portal_ensure_token(),
            "&report_type=%s" % report_type if report_type else "",
            "&download=true" if download else "",
            query_string if query_string else "",
            "#%s" % anchor if anchor else "",
        )

        return url

    def show_opportunity(self):
        self.ensure_one()
        ids = self.x_partner_id.get_partner_leads().ids
        action = {
            "name": self.x_partner_id.name,
            "type": "ir.actions.act_window",
            "res_model": "crm.lead",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", ids]],
        }
        return action

    @api.depends("x_partner_id")
    def _compute_x_opportunity_ids(self):
        for rec in self:
            rec.x_opportunity_ids = ", ".join([str(i.id) for i in rec.x_partner_id.get_partner_leads()])

    @api.depends("x_partner_id")
    def _compute_count_opportunity_id(self):
        for rec in self:
            rec.count_opportunity_id = len(rec.x_partner_id.get_partner_leads())

    def stringify(self):
        # Filtering of record here may not be need. it was added not to
        # break the logic transfer from the website to here
        orders = self.filtered(lambda r: r.state not in ["draft", "sent"])
        names = ", ".join([order.name for order in orders])
        return names


class SaleOrderLine(models.Model):
    """."""

    _inherit = "sale.order.line"

    stock_move_id = fields.Many2one(comodel_name="stock.move", compute="_compute_stock_move_id")
    product_state = fields.Selection(
        selection=STATES, string="Estado", compute="_compute_product_state", default="approved"
    )
    x_qty_received = fields.Float(string="Cantidad Recibida", compute="_compute_qty_received_with_uom_id")
    x_qty_received_uom_id = fields.Many2one(comodel_name="uom.uom", compute="_compute_qty_received_with_uom_id")
    x_ordered_quantity = fields.Float(string="Cantidad Pedida", compute="_compute_qty_received_with_uom_id")
    x_date_expected = fields.Date(string="Fecha Esperada", compute="_compute_x_date_expected")

    @api.depends("order_id")
    def _compute_qty_received_with_uom_id(self):
        purchase_line = self.env["purchase.order.line"]
        for rec in self:
            origin = rec.mapped("order_id").name
            domain = [("order_id.origin", "=", origin), ("product_id", "=", rec.product_id.id)]
            # line = purchase_line.search(domain, limit=1, order="id desc")
            line = purchase_line.search(domain, order="id desc")
            rec.x_qty_received = sum(line.mapped("qty_received"))
            rec.x_qty_received_uom_id = len(line) > 0 and line[0].product_uom.id or False
            rec.x_ordered_quantity = sum(line.mapped("product_qty"))

    def _compute_stock_move_id(self):
        for rec in self:
            po_domain = ["|", ("group_id.name", "=", rec.order_id.name), ("origin", "=", rec.order_id.name)]
            purchase = self.env["purchase.order"].search(po_domain)
            purchase_names = [po.name for po in purchase]
            domain = [
                ("product_id", "=", rec.product_id.id),
                ("origin", "in", purchase_names),
                ("group_id.name", "=", rec.order_id.name),  # Enable on live for more accuracy
                ("picking_type_id.sequence_code", "=", "IN"),
            ]
            stock_move = self.env["stock.move"].search(domain, limit=1, order="date_expected desc")
            rec.stock_move_id = stock_move.id

    @api.depends("product_id", "order_id.name")
    def _compute_product_state(self):

        purchase_line = self.env["purchase.order.line"]
        picking = self.env["stock.picking"]
        for rec in self:
            origin = rec.mapped("order_id").name
            domain = [("order_id.origin", "=", origin), ("product_id", "=", rec.product_id.id)]
            line = purchase_line.search(domain, limit=1, order="id desc")

            if rec.x_ordered_quantity == rec.stock_move_id.quantity_done:
                rec.product_state = "delivered"
            elif rec.x_ordered_quantity <= rec.x_qty_received:
                rec.product_state = "at warehouse"
            elif line.order_id.falta_confirmacion == True:
                rec.product_state = "approved"
            else:
                rec.product_state = "processed"

    @api.depends("product_id")
    def _compute_x_date_expected(self):
        for rec in self:
            purchase = self.env["purchase.order"].search([("group_id.name", "=", rec.order_id.name)])
            purchase_names = [po.name for po in purchase]
            domain = [
                ("product_id", "=", rec.product_id.id),
                ("origin", "in", purchase_names),
                ("group_id.name", "=", rec.order_id.name),
                ("picking_type_id.sequence_code", "=", "IN"),
            ]
            stock_move = self.env["stock.move"].search(domain, order="date_expected desc", limit=1)

            if rec.product_state == "approved":
                rec.x_date_expected = False
            else:
                rec.x_date_expected = stock_move.date_expected
