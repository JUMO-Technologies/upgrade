import logging
import odoo

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = odoo.api.Environment(cr, 1, {})
    orders = env["purchase.order"].search([])
    for order in orders:
        order.write({"falta_confirmacion": order.x_studio_field_Wj1eI})
