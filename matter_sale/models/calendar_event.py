# -*- coding: utf-8 -*-

from odoo import fields, models, api


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    sale_team_id = fields.Many2one("crm.team", string="Sales Team", compute="_compute_sale_team", store=True)

    @api.depends("partner_id")
    def _compute_sale_team(self):
        for event in self:
            team = False
            crm_obj = self.env['crm.team']
            if event.partner_id.team_id:
                team = event.partner_id.team_id
            users = event.partner_id.user_ids
            if not team and users:
                team = crm_obj._get_default_team_id(users[0].id)
            user = event.partner_id.user_id
            if not team and user:
                team = crm_obj._get_default_team_id(user.id)
            if team:
                event.sale_team_id = team
            else:
                event.sale_team_id = False
