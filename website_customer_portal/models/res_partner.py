from odoo import models, fields, api, SUPERUSER_ID


class ResPartner(models.Model):
    """."""

    _name = "res.partner"
    _inherit = ["portal.mixin", "res.partner"]
    contact_info = fields.Char(string="Contact Info")
    contact_info_phone = fields.Char(string="Contact Phone")

    def get_partner_leads(self):
        sales = (
            self.env["sale.order"]
            .with_user(SUPERUSER_ID)
            .read_group(
                [("partner_id", "=", self.id), ("state", "not in", ["draft", "sent"]),],
                ["x_studio_field_RBuAR"],
                ["x_studio_field_RBuAR"],
            )
        )
        ids = [s.get("x_studio_field_RBuAR") for s in sales if s.get("x_studio_field_RBuAR")]
        leads = self.env["crm.lead"].with_user(SUPERUSER_ID).search([("name", "in", ids)])
        [lead._portal_ensure_token() for lead in leads]
        return leads

    def _compute_access_url(self):
        super(ResPartner, self)._compute_access_url()
        for partner in self:
            partner.access_url = "/my/%s/dashboard" % (partner._name,)

    def preview_opportunity(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "target": "self",
            "url": self.get_portal_url(),
        }
