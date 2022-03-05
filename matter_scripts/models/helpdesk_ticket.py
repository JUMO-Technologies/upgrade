from odoo import models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def script_recompute_all_teams(self):
        # GET VISIT
        projects = self.env['x_proyecto']
        self.env.add_to_compute(projects._fields['x_studio_field_6gMg9'], projects.search([]))
        visits = self.env['x_registro']
        self.env.add_to_compute(visits._fields['x_studio_field_GXF3Z'], visits.search([]))
        tickets = self.env['helpdesk.ticket']
        self.env.add_to_compute(tickets._fields['x_studio_field_e4Qt9'], tickets.search([]))
