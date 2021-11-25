from odoo import models, fields, api, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    # Description : make it stored to use it in the kanban view order attribute
    activity_date_deadline = fields.Date(store=True)
    # Studio
    prioridad = fields.Selection([
        ('0', 'Muy baja'),
        ('1', 'Baja'),
        ('2', 'Normal'),
        ('3', 'Alta'),
        ('4', 'Muy Alta')
    ])
    activity_date_deadline = fields.Date(store=True)

    score = fields.Integer(string="Computed score", compute="_compute_score", store=True)

    @api.depends('prioridad')
    def _compute_score(self):
        for rec in self:
            if not rec.prioridad:
                rec.score = 1
            else:
                rec.score = int(rec.prioridad)+1
