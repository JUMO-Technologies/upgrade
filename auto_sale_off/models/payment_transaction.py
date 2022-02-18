import logging

from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _check_amount_and_confirm_order(self):
        self.ensure_one()
        for order in self.sale_order_ids.filtered(lambda so: so.state in ("draft", "sent")):
            if order.confirm_after_payment:
                if order.currency_id.compare_amounts(self.amount, order.amount_total) == 0:
                    order.with_context(send_email=True).action_confirm()
                else:
                    _logger.warning(
                        "<%s> transaction AMOUNT MISMATCH for order %s (ID %s): expected %r, got %r",
                        self.acquirer_id.provider,
                        order.name,
                        order.id,
                        order.amount_total,
                        self.amount,
                    )
                    order.message_post(
                        subject=_("Amount Mismatch (%s)", self.acquirer_id.provider),
                        body=_(
                            "The order was not confirmed despite response from the acquirer (%s): "
                            "order total is %r but acquirer replied with %r."
                        ) % (
                            self.acquirer_id.provider,
                            order.amount_total,
                            self.amount,
                        ),
                    )
