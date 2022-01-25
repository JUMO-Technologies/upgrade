from datetime import datetime

from odoo import fields, models, api


class AccountFinancialReportLine(models.Model):
    _inherit = 'account.financial.html.report.line'

    def _get_with_statement(self):
        sql_with, with_params = super(AccountFinancialReportLine, self)._get_with_statement()
        if with_params:
            with_params[-9] = "%s-12-31" % datetime.strptime(with_params[-9], "%Y-%m-%d").year
            with_params[-8] = "%s-01-01" % datetime.strptime(with_params[-8], "%Y-%m-%d").year
        return sql_with, with_params
