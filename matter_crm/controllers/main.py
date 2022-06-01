import json

from odoo import http
from odoo.http import request
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.exceptions import ValidationError

from datetime import datetime


class HoursError(ValidationError):
    pass


class WebsiteMain(WebsiteForm):

    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True,
                csrf=False)
    def website_form(self, model_name, **kwargs):
        params = request.params
        if "Motivo visita" in params:
            date_value = params.get("Fecha y Hora", False)
            if date_value:
                date_value = datetime.strptime(date_value, "%d/%m/%Y %H:%M:%S")
                if date_value.weekday() in (5, 6):
                    return json.dumps({'error_fields': "No puede seleccionar esta fecha, verifique nuestros horario"})
        return super(WebsiteMain, self).website_form(model_name, **kwargs)
