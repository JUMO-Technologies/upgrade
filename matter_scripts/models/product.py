from odoo import models

COLLECTION_DICT = {
    1477: 'Matter Atelier - Mithril',
    1031: 'Matter Atelier - Nuathwood',
    1134: 'Matter Atelier - Yosemite Wood',
    1141: 'Matter Atelier - Nobilato',
    1163: 'Matter Atelier - Inalco - Petra',
    1164: 'Matter Atelier - Inalco - Iseo',
    1165: 'Matter Atelier - Inalco - Foster',
    1166: 'Matter Atelier - Lorien',
    1167: 'Matter Atelier - Baobil',
    1168: 'Matter Atelier - Nicia',
    1170: 'Matter Atelier - Edoras',
    1172: 'Matter Atelier - Deli',
    1173: 'Matter Atelier - Alkum',
    1174: 'Matter Atelier - Fleet',
    1175: 'Matter Atelier - Montorise',
    1178: 'Matter Atelier - Manau',
    1180: 'Matter Atelier Terracota E',
    1183: 'Matter Atelier - Intoio',
    1190: 'Matter Atelier - Valar',
    1205: 'Matter Atelier - Finex',
    1208: 'Matter Atelier - Nundu',
    1215: 'Matter Atelier - Ainurwood',
    1221: 'Matter Atelier - Trilogía',
    1222: 'Matter Atelier - Kuha',
    1254: 'Matter Atelier - Jump',
    1259: 'Matter Atelier - Intelle',
    1288: 'Matter Atelier - Grace',
    1295: 'Matter Atelier - Renoir',
    1300: 'Matter Atelier - Deep',
    1491: 'Matter Atelier - Ogetti',
    1501: 'Matter Atelier - Sommer',
    1569: 'Matter Atelier - Diadoné',
    1572: 'Matter Atelier - Migra',
    1610: 'Matter Atelier - Urali',
    1623: 'Matter Atelier - Mutina Tierras',
    1651: 'Matter Atelier - Mutina Déchirer',
    1652: 'Matter Atelier - Mutina Rombini',
    1670: 'Matter Atelier - Savoir',
    1672: 'Matter Atelier - Marmi',
    1674: 'Matter Atelier - Assolut',
    1677: 'Matter Atelier - Ottenta',
    1679: 'Matter Atelier - Metope',
    1683: 'Matter Atelier - Xenocris',
    1685: 'Matter Atelier - Astrain',
    1695: 'Matter Atelier - Gurp',
    1710: 'Matter Atelier Terracota LL',
    1767: 'Inbani - Giro',
    1862: 'Matter Atelier - Mutina Pico',
    1916: 'Matter Atelier - Tralente Mix',
    1949: 'Matter Atelier - Isosceles',
    1983: 'Matter Atelier - Mutina Celosia',
    2017: 'Matter Atelier - Tormin',
    2049: 'Matter Atelier - Pikeless',
    2073: 'Matter Atelier - Lenox',
    212: 'Matter Atelier - Sanmarco',
    2228: 'Matter Atelier - Lutum',
    2230: 'Matter Atelier - Somos',
    2308: 'Matter Atelier - Movi',
    2324: 'Matter Atelier - Mutina Primavera',
    2384: 'Matter Atelier - Mutina Diarama',
    2394: 'Matter Atelier - Chaplin',
    2411: 'Matter Atelier - Quezon',
    2419: 'Matter Atelier - Mutina Tape',
    2444: 'Matter Atelier Gres natural T',
    2452: 'Matter Atelier - Terracota V',
    2459: 'Matter Atelier - Terracota AC',
    418: 'Matter Atelier - Poluss',
    460: 'Matter Atelier - Tenere',
    508: 'Matter Atelier - Cave',
    509: 'Matter Atelier - Liger',
    525: 'Matter Atelier - Loop',
    559: 'Matter Atelier - Cheret',
    590: 'Matter Atelier - Care',
    633: 'Matter Atelier - Loopwall',
    666: 'Matter Atelier - Olinville Cement',
    667: 'Matter Atelier - Olinville Marble',
    671: 'Matter Atelier - Cruagh Wood',
    692: 'Matter Atelier - Lanat Wall',
    742: 'Matter Atelier - Izola',
    744: 'Matter Atelier - Terracota Esmaltada',
    754: 'Matter Atelier - Beans Rustic',
    756: 'Matter Atelier - Ailan',
    761: 'Matter Atelier - Sanzio',
    767: 'Matter Atelier - Naboo',
    773: 'Matter Atelier - Mutina Puzzle',
    780: 'Matter Atelier - Borni',
    796: 'Matter Atelier - Estric',
    798: 'Matter Atelier - Lunatica',
    828: 'Matter Atelier - Graffiti',
    839: 'Matter Atelier - Fresco',
    843: 'Matter Atelier - Canaletto',
    848: 'Matter Atelier - Túrin',
    854: 'Matter Atelier - Joshua',
    869: 'Matter Atelier - Nimwood',
    880: 'Matter Atelier - Esentica',
    896: 'Matter Atelier - Mutina Azulej',
    899: 'Matter Atelier - Braque Pastel',
    902: 'Matter Atelier - Mairea',
}


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
        OR POSITION(xac.x_name IN prod.name) = 0
        OR POSITION(prod.x_product_name_desc IN prod.name) = 0)
        AND prod.active = true) AS prods"""


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    def script_rename_error_category(self):
        if not self.user_has_groups("base.group_system"):
            return
        collection_obj = self.env['product.public.category']
        for key, value in COLLECTION_DICT.items():
            coll = collection_obj.browse(key)
            if coll:
                sql = "UPDATE product_public_category SET name = %s WHERE id = %s"
                sql2 = """UPDATE ir_translation SET src = %s WHERE res_id = %s 
                AND name = 'product.public.category,name'"""
                self._cr.execute(sql, (value, key))
                self._cr.execute(sql2, (value, key))
