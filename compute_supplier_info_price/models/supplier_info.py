from odoo import api, fields, models


class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    discount_1 = fields.Float(string='Discount 1')
    discount_2 = fields.Float(string='Discount 2')
    discount_3 = fields.Float(string='Discount 3')
    price = fields.Float(compute='_get_price', store=True)
    compute_price = fields.Float(string='Price without Discount')

    @api.depends('discount_1', 'discount_2', 'discount_3', 'compute_price')
    def _get_price(self):
        for record in self:
            record['price'] = record.compute_price * (1 - record.discount_1 / 100.) * (1 - record.discount_2 / 100.) * (1 - record.discount_3 / 100.)
