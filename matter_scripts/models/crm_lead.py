from odoo import models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _recompute_leads_customer(self):
        leads = self.env['crm.lead']
        self.env.add_to_compute(leads._fields['x_studio_field_6gMg9'], leads.search([]))
