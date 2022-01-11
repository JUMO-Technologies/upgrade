from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_product_name_desc = fields.Text()


class Product(models.Model):
    _inherit = "product.product"

    image_url = fields.Char(string="Image URL", compute="_compute_image_url_link")

    def _compute_image_url_link(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")

        for rec in self:
            rec.image_url = "%s/web/image/product.template/%s/image_1920" % (base_url, rec.product_tmpl_id.id)
