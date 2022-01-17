from odoo.http import route, request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import SUPERUSER_ID


class CustomerPortal(CustomerPortal):
    def _prepare_lead_portal_values(self, leads):
        values = self._prepare_home_portal_values()

        values.update(leads=leads, lead_count=len(leads))
        return values

    def _prepare_dashboard_portal_values(self, access_token):
        values = self._prepare_home_portal_values()
        domain = [("access_token", "=", access_token)]
        lead_id = request.env["crm.lead"].with_user(SUPERUSER_ID).search(domain)
        values.update(lead_sales=lead_id.get_sale_by_oppotunity_id(lead_id), lead_id=lead_id)
        return values

    @route(
        ["/my/dashboard", "/my/<string:model>/dashboard", "/my/dashboard/<string:lead_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def dashboard(self, model=None, lead_id=None, access_token=None, **kw):
        access_token = access_token or request.httprequest.args.get("access_token")
        partner = request.env["res.partner"]
        if access_token:
            if model == "res.partner":
                partner = request.env["res.partner"].search([("access_token", "=", access_token)], limit=1)
            elif model == "sale.order":
                order = (
                    request.env["sale.order"]
                    .with_user(SUPERUSER_ID)
                    .search([("access_token", "=", access_token)], limit=1)
                )
                partner = order.x_partner_id
        leads = partner.get_partner_leads() or request.env.user.partner_id.get_partner_leads()
        if not lead_id:
            values = self._prepare_lead_portal_values(leads)
            return request.render("website_customer_portal.portal_my_dashboard", values)
        else:
            values = self._prepare_dashboard_portal_values(lead_id)
            return request.render("website_customer_portal.portal_my_dashboard_main", values)
