from . import models


def _post_init_copy_discount(cr, registry):
    cr.execute("UPDATE sale_order_line SET discount1 = discount;")
    cr.execute("UPDATE account_move_line SET discount1 = discount;")
