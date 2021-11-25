import logging
import os

from odoo import SUPERUSER_ID, api
from odoo.addons.crm_matter.migrations import util

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    if "ODOO_STAGE" in os.environ and os.environ['ODOO_STAGE'] == "dev":
        _logger.info('Exit migration script : dev env database !')
        return ""

    _logger.info('###################################################################################')
    _logger.info('Begin pre_10')
    _logger.info('----------RENAME FIELDS----------')

    to_rename_fields = (
                       ('crm.lead', 'x_studio_field_ERcE7', 'prioridad'),
    )

    for field in to_rename_fields:
        cr.execute("UPDATE ir_model_fields SET state='base' WHERE name LIKE '%s' AND model LIKE '%s'" % (field[1], field[0]))
        util.rename_field(cr, field[0], field[1], field[2])
        _logger.info('rename field : %s -> %s on model %s' % (field[1], field[2], field[0]))

    cr.execute("UPDATE crm_lead SET prioridad='0' WHERE prioridad='Muy baja';")
    cr.execute("UPDATE crm_lead SET prioridad='1' WHERE prioridad='Baja';")
    cr.execute("UPDATE crm_lead SET prioridad='2' WHERE prioridad='Normal';")
    cr.execute("UPDATE crm_lead SET prioridad='3' WHERE prioridad='Alta';")
    cr.execute("UPDATE crm_lead SET prioridad='4' WHERE prioridad='Muy Alta';")
    cr.execute("DELETE FROM ir_model_fields_selection WHERE field_id=8371 and id in(478,479,480,481,482);")

    # Mig field in studio views :
    cr.execute("UPDATE ir_ui_view SET arch_db = REPLACE(arch_db, 'x_studio_field_ERcE7', 'prioridad') WHERE id in(1667, 1679, 1574)")