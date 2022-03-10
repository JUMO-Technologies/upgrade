from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def script_rename_product(self):
        if not self.user_has_groups("base.group_system"):
            return
        sql = """UPDATE ir_translation it SET src = prods.name, value = '' {} 
        WHERE it.res_id = prods.id AND it.name = 'product.public.category,name';
        """.format(self._get_from_clause())

        sql2 = """UPDATE product_template pt SET name = prods.name {}
        WHERE pt.id = prods.id;""".format(self._get_from_clause())
        self._cr.execute(sql)
        self._cr.execute(sql2)

    def _get_from_clause(self):
        return """FROM (SELECT prod.id, CONCAT(xc.collection_number, ' ', xc.name, ' ', xcc.x_name, ' ', 
        xfc.x_name, ' ',  CASE WHEN prod.x_product_rect THEN 'R ' ELSE '' END, xac.x_name, ' ', 
        prod.x_product_name_desc) AS name
        FROM product_template prod
        INNER JOIN product_public_category xc ON xc.id = prod.public_category_id
        INNER JOIN x_colores_coleccion xcc ON xcc.id = prod.x_producto_color
        INNER JOIN x_formatos_coleccion xfc ON xfc.id = prod.x_producto_formato
        INNER JOIN x_acabados_coleccion xac ON xac.id = prod.x_producto_acabado
        WHERE (POSITION(xcc.x_name IN prod.name) = 0
        OR POSITION(xfc.x_name IN prod.name) = 0
        OR POSITION(xac.x_name IN prod.name) = 0)
        AND prod.active = true) AS prods"""
