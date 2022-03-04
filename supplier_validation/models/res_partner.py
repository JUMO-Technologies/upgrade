from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    po_validation = fields.Boolean(string="Validación por PO")
    product_validation = fields.Boolean(string="Validación por producto")
