from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_template_id = fields.Many2one(default=lambda s: s.env.company.sale_order_template_id)

    @api.model
    def _del_default_sale_order_template(self):
        IrDefault = self.env['ir.default']
        if IrDefault.get('sale.order', 'sale_order_template_id'):
            field_id = self.env['ir.model.fields'].search([('model', '=', 'sale.order'),
                                                           ('name', '=', 'sale_order_template_id')])
            default_vls = IrDefault.search([('field_id', '=', field_id.id)])
            if default_vls:
                default_vls.unlink()
