from odoo import fields, models, api


class CrmLead(models.Model):
    _inherit = "crm.lead"

    partner_category_ids = fields.Many2many("res.partner.category", string="Etiqueta")
    visit_mail_sent = fields.Boolean(default=False)

    def write(self, values):
        res = super(CrmLead, self).write(values)
        if 'description' in values:
            if "Motivo visita" in values["description"]:
                template = self.env.ref("matter_crm.visit_send_email")
                for lead in self:
                    if not lead.visit_mail_sent and lead.contact_name and lead.email_from:
                        template.send_mail(lead.id, force_send=True, raise_exception=False)
                        lead.visit_mail_sent = True
        return res
