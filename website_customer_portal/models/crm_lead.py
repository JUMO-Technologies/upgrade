import logging

from odoo import models, fields, api
from odoo.models import lazy_name_get

_logger = logging.getLogger(__name__)


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

    @api.model
    def _add_field(self, name, field):
        res = super(CRMLead, self)._add_field(name, field)

        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        # private implementation of name_search, allows passing a dedicated user
        # for the name_get part to solve some access rights issues
        args = list(args or [])
        # optimize out the default criterion of ``ilike ''`` that matches everything
        if not self._rec_name:
            _logger.warning("Cannot execute name_search, no _rec_name defined on %s", self._name)
        elif not (name == '' and operator == 'ilike'):
            values = [name]
            if name:
                values = name.split("-", maxsplit=1)
            len_vals = len(values)
            if len_vals == 1:
                vals0 = values[0].strip()
                args += ['|', ("id", operator, vals0), ("name", operator, vals0)]
            elif len_vals > 1:
                vals0 = values[0].strip()
                vals1 = values[1].strip()
                args += ['|', '|', ("id", operator, vals0), ("id", operator, vals1),
                         '|', ("name", operator, vals0), ("name", operator, vals1)]
        ids = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        recs = self.browse(ids)
        return lazy_name_get(recs.with_user(name_get_uid))
