import odoo
from odoo.http import route, request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import SUPERUSER_ID, http, _

from odoo.addons.web.controllers.main import ensure_db
from odoo.addons.web.controllers.main import Home


class CustomerPortal(CustomerPortal):
    def _prepare_lead_portal_values(self, leads):
        values = self._prepare_home_portal_values()
        values.update(leads=leads, lead_count=len(leads))
        return values

    def _prepare_dashboard_portal_values(self, access_token):
        values = self._prepare_home_portal_values()
        domain = [("access_token", "=", access_token),
                  ('stage_id.hide_from_delivery_portal', '!=', True)]
        lead_id = request.env["crm.lead"].with_user(SUPERUSER_ID).search(domain)
        down_payment = int(request.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id'))
        values.update(lead_sales=lead_id.get_sale_by_oppotunity_id(lead_id), lead_id=lead_id, down_payment=down_payment)
        return values

    @route(["/my/dashboard", "/my/<string:model>/dashboard", "/my/dashboard/<string:lead_id>"],
           type="http", auth="user", website=True)
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

    @route(["/my/dashboard/login", "/my/<string:model>/dashboard/login", "/my/dashboard/<string:lead_id>/login"],
           type="http", auth="public", website=True)
    def my_delivery_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                   request.params['password'])
                request.params['login_success'] = True
                home = Home()
                return http.redirect_with_hash(home._login_redirect(uid, redirect="/my/dashboard"))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('website_customer_portal.my_login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
