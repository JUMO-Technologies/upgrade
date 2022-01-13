from odoo import models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if res:
            if res.supplier_rank > 0:
                company = self.env.company
                res.with_context(order_company=company)._auto_create_supplier_account()
        return res

    def _auto_create_customer_account(self):
        self.ensure_one()
        company = self._context.get('order_company', False)
        if not company:
            return False
        default_account_receivable = company.partner_id.property_account_receivable_id.id
        if default_account_receivable != self.property_account_receivable_id.id:
            return False

        sequence_code = str(self.id).zfill(4)
        code = self.property_account_receivable_id.code
        code_account = (code[0:4])
        account_values = {
            'code': code_account + sequence_code,
            'name': self.name,
            'user_type_id': self.env['account.account.type'].search([('type', '=', 'receivable')]).id or None,
            'group_id': self.env['account.group'].search([('code_prefix', '=', '4300')]).id or None,
            'reconcile': True,
        }
        new_account = self.env['account.account'].sudo().create(account_values)
        if new_account:
            partner_values = {'property_account_receivable_id': new_account.id}
            if not self.customer_rank:
                partner_values['customer_rank'] = 1
            self.write(partner_values)

    def _auto_create_supplier_account(self):
        self.ensure_one()
        company = self._context.get('order_company', False)
        if not company:
            return False
        default_account_payable = company.partner_id.property_account_payable_id.id
        if default_account_payable != self.property_account_payable_id.id:
            return False
        sequence_code = str(self.id).zfill(4)
        code = self.property_account_payable_id.code
        code_account = (code[0:4])
        account_values = {
            "code": code_account + sequence_code,
            "name": self.name,
            "user_type_id": self.env['account.account.type'].search([('type', '=', 'receivable')]).id or None,
            'reconcile': True,
        }
        new_account = self.env['account.account'].sudo().create(account_values)
        if new_account:
            partner_values = {'property_account_payable_id': new_account.id}
            if not self.supplier_rank:
                partner_values['supplier_rank'] = 1
            self.write(partner_values)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if res:
            res.partner_id.with_context(order_company=res.company_id)._auto_create_customer_account()
        return res
