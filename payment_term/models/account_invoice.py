from odoo import api, fields, models

#from datetime import datetime
import datetime
import dateutil


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    other_payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Special Payment Term',
        domain=[('special_term', '=', True)]
    )

    def _calculate_due_date(self):
        for move in self:
            if move.other_payment_term_id and move.other_payment_term_id.special_term and move.other_payment_term_id.number_days and move.other_payment_term_id.day_month:
                invoice_date = move.invoice_date or fields.date.today()
                due_date = invoice_date + datetime.timedelta(days=move.other_payment_term_id.number_days)

                if due_date.day > move.other_payment_term_id.day_month:
                    due_date += dateutil.relativedelta.relativedelta(months=+1)

                due_date = due_date.replace(day=move.other_payment_term_id.day_month)
                move.invoice_date_due = due_date

    def _set_payment_term(self):
        for move in self:
            if move.state == 'draft' and move.invoice_origin:
                invoice_origin = move.invoice_origin.split(':')[0]
                so = self.env['sale.order'].search([
                    ('name', '=', invoice_origin)
                ], limit=1)

                if so and so.other_payment_term_id:
                    move.write({
                        'other_payment_term_id': so.payment_term_id.id,
                        'invoice_payment_term_id': False
                    })
                else:
                    po = self.env['purchase.order'].search([
                        ('name', '=', invoice_origin)
                    ], limit=1)
                    if po and po.other_payment_term_id:
                        move.write({
                            'other_payment_term_id': po.payment_term_id.id,
                            'invoice_payment_term_id': False
                        })

    @api.onchange('other_payment_term_id')
    def onchange_other_payment_term(self):
        if self.other_payment_term_id and self.invoice_payment_term_id:
            self['invoice_payment_term_id'] = False

            invoice_date = self.invoice_date or fields.date.today()
            due_date = invoice_date + datetime.timedelta(days=self.payment_term_id.number_days)
            if due_date.day > self.other_payment_term_id.day_month:
                due_date += dateutil.relativedelta.relativedelta(months=+1)
            due_date = due_date.replace(day=self.other_payment_term_id.day_month)
            self['invoice_date_due'] = due_date

    @api.onchange('invoice_payment_term_id')
    def onchange_invoice_payment_term_id(self):
        if self.invoice_payment_term_id and self.other_payment_term_id:
            self['other_payment_term_id'] = False

    @api.onchange('partner_id')
    def onchange_partner(self):
        if self.partner_id and self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.special_term:
            self['other_payment_term_id'] = self.partner_id.property_payment_term_id.id
            self['invoice_payment_term_id'] = False

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        res._calculate_due_date()
        res._set_payment_term()
        return res

    def write(self, vals):
        res = super(AccountInvoice, self).write(vals)
        self._calculate_due_date()
        return res
