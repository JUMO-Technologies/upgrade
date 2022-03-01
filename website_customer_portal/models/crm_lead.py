from odoo import models, fields, api


class CRMLead(models.Model):
    """."""

    _name = "crm.lead"
    _rec_name = "display_name"
    _inherit = ["crm.lead", "portal.mixin"]

    back_up_specialist = fields.Many2one(
        comodel_name="res.users",
        string="Back Up Specialist",
        domain="[('company_id', '=', company_id), ('groups_id', 'in', [11])]",
    )
    # ask for the group name, hard coding group id this way is bad.
    shipping_address = fields.Text(string="Dirección de envío")
    project_contact = fields.Text(string="Contacto Obra")

    @api.depends("name")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "%s - %s" % (rec.id, rec.name)

    def get_sale_by_oppotunity_id(self, lead_id):
        return self.env["sale.order"].search(
            [("opportunity_id", "=", lead_id.id), ("state", "not in", ["draft", "sent"])]
        )


class CrmStage(models.Model):
    _inherit = "crm.stage"

    hide_from_delivery_portal = fields.Boolean("Ocultar del Portal Delivery", default=False)
