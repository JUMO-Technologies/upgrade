from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    sale_team_id = fields.Many2one("crm.team", string="Sales Team")
