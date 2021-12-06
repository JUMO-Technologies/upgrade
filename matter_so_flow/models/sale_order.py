from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def check_qty(self):
        warehouse = self.env.ref('stock.warehouse0')
        warehouse = warehouse | self.env.ref('__export__.warehouse_showroom')
        make_to_order_id = self.env.ref('stock.route_warehouse0_mto').id
        for record in self:
            for sol in record.order_line:
                if sol.route_id.id != make_to_order_id:
                    res = sol.product_id.with_context(warehouse=warehouse.ids)._compute_quantities_dict(None, None, None)
                    if res.get(sol.product_id.id):
                        qty_max = res[sol.product_id.id]['virtual_available']
                        if qty_max < sol.product_uom_qty:
                            raise UserError('You don\'t have enough of %s. You can sell a maximum of %0.2f %s' % (sol.product_id.name, qty_max, sol.product_uom.name))

            # if we have enough on hand for each sale order line, execute normal process:
            record.action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    forecasted_qty = fields.Integer(
        string='Available quantity',
        compute='_get_forecasted_qty'
    )

    def _get_forecasted_qty(self):
        # warehouse = self.env.ref('stock.warehouse0')
        for rec in self:
            forecasted_qty = rec.product_id.with_context(warehouse=rec.order_id.warehouse_id.id).virtual_available
            rec['forecasted_qty'] = forecasted_qty

    def copy_so(self):
        self.ensure_one()
        self.copy({
            'order_id': self.order_id.id
        })