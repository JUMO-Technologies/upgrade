# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Migrated from x_generic (sol_draft.field_product_template__x_generic)
    generic = fields.Boolean('Generic')
