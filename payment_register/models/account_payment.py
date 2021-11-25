from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    amount_given = fields.Monetary(string='Amount Given')
    amount_return = fields.Monetary(
        string='Amount Return',
        compute='_get_amount_return',
        store=True
    )
    is_cash = fields.Boolean(string='Is Cash', compute='_get_is_cash', store=True)

    @api.depends('amount')
    def _get_amount_return(self):
        for payment in self:
            payment['amount_return'] = (payment.amount_given if payment.amount_given else 0.) - (payment.amount if payment.amount else 0.)

    @api.depends('journal_id', 'journal_id.type')
    def _get_is_cash(self):
        for payment in self:
            payment['is_cash'] = payment.journal_id and payment.journal_id.type == 'cash'
