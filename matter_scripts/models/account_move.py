from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    def _recompute_invoices(self):
        invoices = self.search([])
        if invoices:
            invoices.flush()

    def recompute_all_account_tag(self):
        def _compute_base_line_taxes(base_line):
            ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
            amount_currency & balance could not be the same as the expected currency rate.
            The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
            :param base_line:   The account.move.line owning the taxes.
            :return:            The result of the compute_all method.
            '''
            move = base_line.move_id

            if move.is_invoice(include_receipts=True):
                handle_price_include = True
                sign = -1 if move.is_inbound() else 1
                quantity = base_line.quantity
                is_refund = move.move_type in ('out_refund', 'in_refund')
                price_unit_wo_discount = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
            else:
                handle_price_include = False
                quantity = 1.0
                tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
                is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)
                price_unit_wo_discount = base_line.amount_currency

            balance_taxes_res = base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
                price_unit_wo_discount,
                currency=base_line.currency_id,
                quantity=quantity,
                product=base_line.product_id,
                partner=base_line.partner_id,
                is_refund=is_refund,
                handle_price_include=handle_price_include,
            )

            if move.move_type == 'entry':
                repartition_field = is_refund and 'refund_repartition_line_ids' or 'invoice_repartition_line_ids'
                repartition_tags = base_line.tax_ids.flatten_taxes_hierarchy().mapped(repartition_field).filtered(lambda x: x.repartition_type == 'base').tag_ids
                tags_need_inversion = self._tax_tags_need_inversion(move, is_refund, tax_type)
                if tags_need_inversion:
                    balance_taxes_res['base_tags'] = base_line._revert_signed_tags(repartition_tags).ids
                    for tax_res in balance_taxes_res['taxes']:
                        tax_res['tag_ids'] = base_line._revert_signed_tags(self.env['account.account.tag'].browse(tax_res['tag_ids'])).ids

            return balance_taxes_res
        for company in self.env.user.company_ids:
            for entry in self.with_company(company).search([('move_type', 'in', ['in_invoice', 'out_invoice',
                                                                                'in_refund', 'out_refund'])]):
                for line in entry.line_ids:
                    if not line.tax_repartition_line_id:
                        compute_all_vals = _compute_base_line_taxes(line)
                        self._cr.execute("""DELETE FROM account_account_tag_account_move_line_rel 
                                                WHERE account_move_line_id = %i""" % line.id)
                        if not compute_all_vals['base_tags']:
                            continue
                        for tag in compute_all_vals['base_tags']:
                            self._cr.execute("""
                            INSERT INTO account_account_tag_account_move_line_rel(account_move_line_id, account_account_tag_id)
                            VALUES (%i, %i)""" % (line.id, tag))
                    elif line.tax_repartition_line_id.tag_ids:
                        self._cr.execute("""DELETE FROM account_account_tag_account_move_line_rel 
                                                WHERE account_move_line_id = %i""" % line.id)
                        if not line.tax_repartition_line_id.tag_ids:
                            continue
                        for tag in line.tax_repartition_line_id.tag_ids.ids:
                            self._cr.execute("""INSERT INTO account_account_tag_account_move_line_rel(account_move_line_id, account_account_tag_id)
                                VALUES (%i, %i)""" % (line.id, tag))


