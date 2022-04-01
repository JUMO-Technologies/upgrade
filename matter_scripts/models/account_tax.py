from odoo import fields, models, api, _
import logging

from odoo.exceptions import ValidationError

_logger = logging.Logger(__name__)


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def create(self, vals):
        res = super(AccountTax, self).create(vals)
        if res and not self._context.get('install_mode', False):
            res._create_account_tax_template()
        return res

    def script_create_account_tax_template(self):
        for company in self.env.user.company_ids:
            for tax in self.with_context(company_id=company.id).search([('company_id', '=', company.id), '|', ('active', '=', True),
                                                                        ('active', '=', False)]):
                tax.with_context(company_id=company.id)._create_account_tax_template()
            company.clear_caches()

    def _create_account_tax_template(self):
        self.ensure_one()
        xml_id = self.env['ir.model.data'].search([('model', '=', 'account.tax'), ('res_id', '=', self.id)])
        xml_id_str = xml_id and xml_id.name or ""
        if not xml_id:
            if not self.name:
                raise ValidationError(_("The tax needs a name"))
            suffix = "%s_%i" % (str(self.type_tax_use).replace(" ", "_").lower(), int(self.amount))
            xml_id_str = "%i_account_tax_%i_%s" % (self.env.company.id, self.id, suffix)
            self._cr.execute("""INSERT INTO ir_model_data(name, module, model, res_id, noupdate)
                            VALUES (%s, 'l10n_es', 'account.tax', %s, true)
                            RETURNING id""", (xml_id_str, self.id))

        else:
            if not xml_id.name.startswith("%i_" % self.env.company.id):
                self._cr.execute("UPDATE ir_model_data SET name = %s WHERE id = %s", (
                    "%i_%s" % (self.env.company.id, xml_id.name), xml_id.id)
                                 )
        template_id = xml_id_str.replace("%i_" % self.env.company.id, "", 1)
        tmp_xml_id = self.env['ir.model.data'].search([('model', '=', 'account.tax.template'),
                                                       ('name', '=', template_id)])
        if not tmp_xml_id:
            values = self._get_tax_template_values()
            tax_tmp = self.env['account.tax.template'].create(values)
            self._cr.execute("""INSERT INTO ir_model_data(name, module, model, res_id, noupdate) 
                                                VALUES (%s, 'l10n_es', 'account.tax.template', %s, true)
                                                RETURNING id""", (template_id, tax_tmp.id))

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