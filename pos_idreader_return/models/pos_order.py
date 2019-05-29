# -*- coding: utf-8 -*-
# © 2018 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models, _


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    @api.model
    def search_line_epc(self, product_epc_list):
        self = self.sudo()
        orderlines = []
        order_vals = {}
        is_partial_return = True
        order = False
        for product_epc in product_epc_list:
            line = self.search([
                ('product_epc', '=', product_epc)
            ], order='create_date desc', limit=1)
            if line:
                if order and line.order_id.id != order.id:
                    return {'error': _(
                        'Products readed are from different orders. '
                        'That is not allowed')}
                else:
                    order = line.order_id
                orderlines.append({
                    'discount': line.discount,
                    'id': line.id,
                    'price_subtotal': line.price_subtotal,
                    'price_subtotal_incl': line.price_subtotal_incl,
                    'price_unit': line.price_unit,
                    'product_id': [line.product_id.id,
                                   line.product_id.display_name],
                    'qty': line.qty,
                    'line_qty_returned': line.line_qty_returned,
                    'date_order': line.order_id.date_order,
                    'loy_applied': line.loy_applied,
                    'product_epc': line.product_epc
                })
        if order:
            statements = self.env['account.bank.statement.line'].search([
                ('id', 'in', order.statement_ids.ids)
            ])

            order_vals = {
                'date_order': order.date_order,
                'id': order.id,
                'invoice_id': order.invoice_id.id,
                'name': order.name,
                'partner_id': order.partner_id.id,
                'pos_reference': order.pos_reference,
                'lines': order.lines.ids,
                'statement_ids': statements.ids,
                'amount_total': order.amount_total,
                'return_status': order.return_status,
                'amount_paid': order.amount_paid,
                'amount_return': order.amount_return,
            }
        return {
            'orderlines': orderlines,
            'order': order_vals,
            'is_partial_return': is_partial_return
        }


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create_from_ui(self, orders):
        result = super(PosOrder, self).create_from_ui(orders)
        order_ids = []
        if isinstance(result, dict) and result.get('orders'):
            order_ids = [o['id'] for o in result['orders']]
        elif result and isinstance(result, (list, tuple)) and\
                isinstance(result[0], (int, long)):
            order_ids = result
        for order in self.browse(order_ids):
            for line in order.lines:
                if not line.product_epc and line.original_line_id and \
                        line.original_line_id.product_epc:
                    line.write({
                        'product_epc': line.original_line_id.product_epc
                    })
        return result
