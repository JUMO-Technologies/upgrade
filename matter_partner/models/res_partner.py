from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    newletter = fields.Boolean()
    data_protection_sign = fields.Boolean(string="Firma Protección de Datos")
    parent_protection_sign = fields.Boolean(related="parent_id.data_protection_sign",
                                            string="Firma de Protección de Datos")
