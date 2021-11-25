from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    other_payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Special Payment Term',
        domain=[('special_term', '=', True)]
    )

    @api.onchange('other_payment_term_id')
    def onchange_other_payment_term_id(self):
        if self.other_payment_term_id and self.payment_term_id:
            self['payment_term_id'] = False

    @api.onchange('payment_term_id')
    def payment_term_id_onchange(self):
        if self.payment_term_id and self.other_payment_term_id:
            self['other_payment_term_id'] = False

    @api.onchange('partner_id')
    def partner_id_onchange(self):
        if self.partner_id and self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.special_term:
            self['other_payment_term_id'] = self.partner_id.property_payment_term_id.id
            self['payment_term_id'] = False
