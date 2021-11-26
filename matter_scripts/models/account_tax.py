from odoo import fields, models, api


class AccountTax(models.Model):
    _inherit = "account.tax"

    def create_account_tax_template(self):
        for company in self.env.user.company_ids:
            for tax in self.with_company(company).search([('company_id', '=', company.id), '|', ('active', '=', True),
                                                          ('active', '=', False)]):
                xml_id = self.env['ir.model.data'].search([('model', '=', 'account.tax'), ('res_id', '=', tax.id)])
                if not xml_id:
                    self._cr.execute("""INSERT INTO ir_model_data(name, module, model, res_id, noupdate)
                    VALUES ('%(company_id)i_account_tax_%(tax_id)i_6370beff', 'l10n_es', 'account.tax', %(tax_id)i, true)
                    RETURNING id""" % {'company_id': company.id, 'tax_id': tax.id})
                    xml_id = self.env['account.tax'].browse(self._cr.fetchone()[0])
                else:
                    if not xml_id.name.startswith("%i_" % company.id):
                        self._cr.execute("UPDATE ir_model_data SET name = '%i_%s' WHERE id = %i"
                                         % (company.id, xml_id.name, xml_id.id))
                template_id = xml_id.name.replace("%i_" % company.id, "", 1)
                tmp_xml_id = self.env['ir.model.data'].search([('model', '=', 'account.tax.template'),
                                                               ('name', '=', template_id)])
                if not tmp_xml_id:
                    values = tax._get_tax_template_values()
                    tax_tmp = self.env['account.tax.template'].create(values)
                    self._cr.execute("""INSERT INTO ir_model_data(name, module, model, res_id, noupdate) 
                                        VALUES ('%s', 'l10n_es', 'account.tax.template', %i, true)
                                        RETURNING id""" % (template_id, tax_tmp.id))
            company.clear_caches()

    def _get_tax_template_values(self):
        self.ensure_one()
        return {
            'description': self.description,
            'type_tax_use': self.type_tax_use,
            'name': self.name,
            'chart_template_id': self.env.ref('l10n_es.account_chart_template_common').id,
            'amount': self.amount,
            'amount_type': self.amount_type,
            'tax_group_id': self.tax_group_id.id,
            'invoice_repartition_line_ids': [(0, 0, {
                    'factor_percent': i.factor_percent,
                    'repartition_type': i.repartition_type,
                    'tag_ids': i.tag_ids.ids,
            }) for i in self.invoice_repartition_line_ids],
            'refund_repartition_line_ids': [(0, 0, {
                    'factor_percent': i.factor_percent,
                    'repartition_type': i.repartition_type,
                    'tag_ids': i.tag_ids.ids,
            }) for i in self.refund_repartition_line_ids],
        }