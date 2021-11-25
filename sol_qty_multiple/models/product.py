# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # studio_customization.m2_caja_product_temp_00cb053c-c385-4a20-bb57-c5cab3361419
    ce_product_m2box = fields.Float(String='Unit of measure / Box')
