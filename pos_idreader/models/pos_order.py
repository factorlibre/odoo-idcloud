# -*- coding: utf-8 -*-
# © 2018 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    product_epc = fields.Char('Product EPC', readonly=True, index=True)
