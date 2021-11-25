from odoo.upgrade import util, myutil


def migrate(cr, version):
    myutil.custom_rename_field(cr, 'product.supplierinfo', 'x_discount_1', 'discount_1')
    myutil.custom_rename_field(cr, 'product.supplierinfo', 'x_discount_2', 'discount_2')
    myutil.custom_rename_field(cr, 'product.supplierinfo', 'x_discount_3', 'discount_3')
    myutil.custom_rename_field(cr, 'product.supplierinfo', 'x_price', 'price')
    myutil.custom_rename_field(cr, 'product.supplierinfo', 'x_compute_price', 'compute_price')
