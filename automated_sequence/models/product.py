# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Migrated from x_coleccion (studio_customization.coleccion_product_te_e6235393-4f8a-4f80-9737-6ded79a1ac65)
    # (included field from product.product automatically created)
    public_category_id = fields.Many2one('product.public.category', 'Colección')

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        res.create_sequence()
        return res

    def create_sequence(self):
        for rec in self:
            if not rec.default_code and rec.public_category_id:
                if not rec.public_category_id.sequence_id:
                    rec.public_category_id.create_sequence()
                if rec.public_category_id.sequence_id:
                    rec.default_code = rec.public_category_id.sequence_id._next()


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    # Migrated from x_sequence_id (automated_sequence.field_x_tipos_producto__x_sequence_id)
    sequence_id = fields.Many2one('ir.sequence', 'Automated Sequence', copy=False)

    # Migrated from x_product_type (studio_customization.tipo_de_producto_pro_34bc1ea1-8685-42da-95c2-aab4405752df)
    product_type_id = fields.Many2one('product.type', 'Tipo de producto')

    # Migrated from x_collection_number (studio_customization.numero_de_coleccion__c18602a0-791c-48db-979a-1cf31653854f)
    collection_number = fields.Char('Número de colección')

    @api.model
    def create(self, vals):
        res = super(ProductPublicCategory, self).create(vals)
        if not res.sequence_id:
            res.create_sequence()
        return res

    def create_sequence(self):
        for rec in self:
            if not rec.sequence_id and rec.product_type_id:
                if not rec.product_type_id.sequence_id:
                    rec.product_type_id.create_sequence()
                rec.collection_number = rec.product_type_id.sequence_id._next()
                rec.sequence_id = self.env['ir.sequence'].create({
                    'name': rec.collection_number,
                    'prefix': '%s-' % rec.collection_number,
                    'padding': 3,
                })


class ProductType(models.Model):
    """
    Migrated from studio_customization.x_tipos_producto
    (studio_customization.tipos_producto_990357c4-51f1-455b-9b9d-b7107cf03a95)

    Note : the views were not migrated, because they were created in studio and depend on a menu also created with
    studio and containing other studio stuff (=> to avoid to transfer all studio custos in python modules...)
    On the production database the menu is visible under Sales / colecciones / typos producto
    On an empty DB we can access a product type through a product.public.category
    """
    _name = 'product.type'
    _description = 'Tipos Producto'

    # Migrated from x_name (created manually in database)
    name = fields.Char(required=True, copy=False)  # was not required on SAAS model fields, but was in the form view

    # Migrated from x_product_category (studio_customization.categoria_de_product_0a74bd66-8f0d-4aab-a6a1-048daaf18b07)
    product_category = fields.Char(translate=True, string="Product category")

    # Migrated from x_sequence_id (automated_sequence.field_x_tipos_producto__x_sequence_id)
    sequence_id = fields.Many2one('ir.sequence', 'Automated Sequence', copy=False, readonly=True)

    @api.model
    def create(self, vals):
        res = super(ProductType, self).create(vals)
        res.create_sequence()
        return res

    def create_sequence(self):
        for rec in self:
            if not rec.sequence_id:
                rec.sequence_id = rec.env['ir.sequence'].create({
                    'name': rec.product_category,
                    'prefix': rec.product_category,
                    'padding': 3,
                })
