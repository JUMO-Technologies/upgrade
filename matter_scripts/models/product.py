from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def script_rename_product(self):
        if not self.user_has_groups("base.group_system"):
            return
        self._cr.execute("""SELECT prod.id FROM product_template prod
        INNER JOIN x_colores_coleccion xcc ON xcc.id = prod.x_producto_color
        INNER JOIN x_formatos_coleccion xfc ON xfc.id = prod.x_producto_formato
        INNER JOIN x_acabados_coleccion xac ON xac.id = prod.x_producto_acabado
        WHERE (POSITION(xcc.x_name IN prod.name) = 0
        OR POSITION(xfc.x_name IN prod.name) = 0
        OR POSITION(xac.x_name IN prod.name) = 0
        OR POSITION(prod.x_product_name_desc IN prod.name) = 0)
        AND prod.active = true;""")
        products = self._cr.fetchall()
        if not products:
            return
        products = map(lambda s: s[0], products)
        for item in self.env['product.template'].browse(products):
            if item.x_product_rect == 1:
                item.write({
                    'name': (item.public_category_id and item.public_category_id.collection_number or '') + ' ' + (
                                item.public_category_id and item.public_category_id.name or '') + ' ' + (
                                        item.x_producto_color and item.x_producto_color.x_name or '') + ' ' + (
                                        item.x_producto_formato and item.x_producto_formato.x_name or '') + ' ' + 'R' + ' ' + (
                                        item.x_producto_acabado and item.x_producto_acabado.x_name or '') + ' ' + (
                                        item.x_product_name_desc and item.x_product_name_desc or '')
                })
            else:
                item.write({
                    'name': (item.public_category_id and item.public_category_id.collection_number or '') + ' ' + (
                                item.public_category_id and item.public_category_id.name or '') + ' ' + (
                                        item.x_producto_color and item.x_producto_color.x_name or '') + ' ' + (
                                        item.x_producto_formato and item.x_producto_formato.x_name or '') + ' ' + (
                                        item.x_producto_acabado and item.x_producto_acabado.x_name or '') + ' ' + (
                                        item.x_product_name_desc and item.x_product_name_desc or '')
                })
