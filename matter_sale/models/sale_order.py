from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    team_warehouse_id = fields.Many2one(related="team_id.warehouse_id", string="Team Warehouse")
    warehouse_id = fields.Many2one(domain="[('id', '=', team_warehouse_id)]")
    purchase_ids = fields.One2many('purchase.order', 'sale_order_id')
    purchase_picking_counts = fields.Integer("Number of Purchase Pickings", compute='_compute_purchase_picking_count',
                                             groups='purchase.group_purchase_user')

    @api.depends('order_line.purchase_line_ids')
    def _compute_purchase_picking_count(self):
        for order in self:
            order.purchase_picking_counts = len(order.purchase_ids.mapped('picking_ids'))

    @api.onchange('team_id')
    def _onchange_team_warehouse(self):
        domain = [('id', '=', self.team_id and self.team_id.warehouse_id.id or 0)]
        warehouse = self.warehouse_id.filtered_domain(domain)
        if not warehouse and self.team_id:
            warehouse = self.team_id.warehouse_id
        self.warehouse_id = warehouse

    @api.onchange('company_id')
    def _onchange_company_id(self):
        """
        Re-write to trigger user change after company change
        """
        super(SaleOrder, self)._onchange_company_id()
        self._onchange_team_warehouse()

    @api.constrains('warehouse_id')
    def _constrains_warehouse_team(self):
        for sale in self:
            if sale.state in ['draft', 'sent'] and sale.team_id and sale.warehouse_id and \
                    sale.warehouse_id.id != sale.team_id.warehouse_id.id:
                raise ValidationError(_("The chosen warehouse is not available to this sales team."))

    def action_view_purchase_picking(self):
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        # override the context to get rid of the default filtering on operation type
        purchase_ids = self.purchase_ids
        pick_ids = purchase_ids.mapped('picking_ids')

        if purchase_ids:
            result['context'] = {'default_partner_id': purchase_ids[0].partner_id.id, 'default_origin': purchase_ids[0].name,
                                 'default_picking_type_id': purchase_ids[0].picking_type_id.id}
        # choose the view_mode accordingly
        if not pick_ids or len(pick_ids) > 1:
            result['domain'] = "[('id','in',%s)]" % (pick_ids.ids)
        elif len(pick_ids) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state,view) for state,view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = pick_ids.id
        return result


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    def _replace_product(self):
        for item in self:
            texto = item.name
            buscar = "Matter Barcelona"
            reemplazar_por = "Matter Atelier"
            text_name = texto.replace(buscar, reemplazar_por)
            item.write({'name': text_name})


