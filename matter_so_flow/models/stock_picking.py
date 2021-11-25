from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    def action_done(self):
        # After the migration, the _compute_state() was not trigger for backorder.
        # We force trigger it here
        ret = super(StockPicking, self).action_done()
        self._compute_state()
        return ret