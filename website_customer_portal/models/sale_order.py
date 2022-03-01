from odoo import models, fields, api


STATES = [
    ("approved", "Presupuesto aprobado"),
    ("processed", "En curso"),
    ("at warehouse", "Pedido en almacén"),
    ("delivered", "Entregado"),
]


class SaleOrder(models.Model):
    """."""

    _inherit = "sale.order"

    x_studio_field_RBuAR = fields.Char()
    # The field above was added in with studio, there is need to re-defined it here

    x_opportunity_ids = fields.Char(string="ID de oportunidad", compute="_compute_x_opportunity_ids")
    count_opportunity_id = fields.Integer(string="Count Opportunity", compute="_compute_count_opportunity_id")
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Usuario Delivery")
    full_delivered = fields.Boolean(string="Full Delivered", compute="_compute_full_delivered")

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

    @api.depends("order_line.product_state")
    def _compute_full_delivered(self):
        for order in self:
            order.full_delivered = not any(l.product_state != 'delivered' for l in order.order_line)


class SaleOrderLine(models.Model):
    """."""

    _inherit = "sale.order.line"

    stock_move_id = fields.Many2one(comodel_name="stock.move", compute="_compute_stock_move_id")
    product_state = fields.Selection(
        selection=STATES, string="Estado", compute="_compute_product_state", default="approved"
    )
    x_qty_received = fields.Float(string="Cantidad Recibida", compute="_compute_qty_received_with_uom_id")
    x_date_expected = fields.Date(string="Fecha Esperada", compute="_compute_x_date_expected")

    @api.depends('move_ids.state', 'move_ids.scrapped', 'move_ids.product_uom_qty', 'move_ids.product_uom')
    def _compute_qty_received_with_uom_id(self):
        for line in self:  # TODO: maybe one day, this should be done in SQL for performance sake
            if line.qty_delivered_method == 'stock_move':
                qty = 0.0
                outgoing_moves, incoming_moves = line._get_outgoing_incoming_moves()
                for move in outgoing_moves:
                    qty += move.product_uom._compute_quantity(move.reserved_availability, line.product_uom,
                                                              rounding_method='HALF-UP')
                for move in incoming_moves:
                    qty -= move.product_uom._compute_quantity(move.reserved_availability, line.product_uom,
                                                              rounding_method='HALF-UP')
                line.x_qty_received = qty
            else:
                line.x_qty_received = 0.0

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
        # picking = self.env["stock.picking"]
        for rec in self:
            if rec.product_uom_qty <= rec.qty_delivered:
                rec.product_state = "delivered"
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
                ("location_id.usage", "=", "supplier"),
            ]
            stock_move = self.env["stock.move"].search(domain, order="date_expected desc", limit=1)

            if rec.product_state == "approved":
                rec.x_date_expected = rec.order_id.commitment_date
            else:
                rec.x_date_expected = stock_move.date_expected
