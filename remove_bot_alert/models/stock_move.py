from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _delay_alert_log_activity(self, mode, move_orig):
        """Post a delay alert next activity on the documents linked to `self`. If the delay alert
        is already present on the document, it isn't posted twice.

        :param mode: 'auto' or 'manual' as a string
        :param move_orig: the stock move triggering the delay alert on the next document
        """
        pass
