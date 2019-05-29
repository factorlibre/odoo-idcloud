# -*- coding: utf-8 -*-
# © 2018 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from datetime import datetime
from odoo import api, fields, models
from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    idcloud_token = fields.Char(
        'IdCloud Token', compute='_get_idcloud_token_store', readonly=True)
    idcloud_location = fields.Char(
        'IdCloud Store', compute='_get_idcloud_token_store', readonly=True)

    @api.multi
    def _get_idcloud_token_store(self):
        idcloud_store_env = self.env['idcloud.store'].sudo()
        idcloud_location_env = self.env['idcloud.location'].sudo()
        for config in self:
            if config.iface_idreader:
                token = self.env['idcloud.backend'].sudo().search(
                    [], limit=1).read(['auth_token'])[0]['auth_token']
                location_id = config.stock_location_id.id
                if not location_id:
                    location_id = config.warehouse_id.lot_stock_id.id
                idcloud_location = idcloud_store_env.sudo().search([
                    ('location_id', '=', location_id)
                ], limit=1)
                if not idcloud_location:
                    idcloud_location = idcloud_location_env.sudo().search([
                        ('location_id', '=', location_id)
                    ], limit=1)
                if idcloud_location:
                    config.idcloud_location = idcloud_location.external_id
                config.idcloud_token = token


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def create_picking(self):
        self_context = self.with_context(connector_no_export=True)
        return super(PosOrder, self_context).create_picking()

    @api.model
    def create_from_ui(self, orders):
        result = super(PosOrder, self).create_from_ui(orders)
        order_ids = []
        if isinstance(result, dict) and result.get('orders'):
            order_ids = [o['id'] for o in result['orders']]
        elif result and isinstance(result, (list, tuple)) and\
                isinstance(result[0], (int, long)):
            order_ids = result
        idcloud_store_env = self.env['idcloud.store']
        idcloud_location_env = self.env['idcloud.location']
        for order in self.browse(order_ids):
            idcloud_location = idcloud_store_env.sudo().search([
                ('location_id', '=', order.location_id.id)
            ], limit=1)
            if not idcloud_location:
                idcloud_location = idcloud_location_env.sudo().search([
                    ('location_id', '=', order.location_id.id)
                ], limit=1)
            # Is necessary to have the location mapped with the store
            if not idcloud_location:
                _logger.warning(
                    'IDCLoud Location Not configured for %s' %
                    order.location_id.complete_name)
                continue
            if order.test_paid():
                # Sell/return products only if order is paid
                for line in order.lines:
                    if not line.product_epc:
                        continue
                    operation = 'sell'
                    if line.qty < 0:
                        operation = 'return'
                    with idcloud_location.backend_id.work_on(
                            line._name) as work:
                        adapter = work.component(
                            usage='idcloud.transaction.adapter')
                        data = {
                            'epc_hex': line.product_epc,
                            'biz_location': idcloud_location.external_id,
                            'timestamp': datetime.now().isoformat()
                        }
                        try:
                            if operation == 'sell':
                                adapter.item_sell(data=data)
                                _logger.info(
                                    'Setting epc %s as sell' %
                                    line.product_epc)
                            elif operation == 'return':
                                adapter.item_return(data=data)
                                _logger.info(
                                    'Setting epc %s as returned' %
                                    line.product_epc)
                        except:
                            # If IdCloud operation fails continue with the
                            # creation of pos.order
                            pass
        return result


class IDCloudTransactionAdapter(Component):
    _name = 'idcloud.transaction.adapter'
    _inherit = 'idcloud.adapter'
    _apply_on = 'pos.order.line'
    _usage = 'idcloud.transaction.adapter'

    _api_endpoint = '/transaction'
    _list_node_name = None
    _external_id_field = None

    def item_sell(self, data=None, params=None):
        api_path = 'v1/sell'
        url = "%s/%s" % (self._api_endpoint, api_path)
        return self._call(url, params=params,
                          data=data, method='POST')

    def item_return(self, data=None, params=None):
        api_path = 'v1/return'
        url = "%s/%s" % (self._api_endpoint, api_path)
        return self._call(url, params=params,
                          data=data, method='POST')
