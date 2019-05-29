# -*- coding: utf-8 -*-
# © 2018 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, exceptions, fields, models, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    iface_idreader = fields.Boolean(
        string='!D Reader', help="Reads RFID tags with !D Reader")
    idreader_region = fields.Selection(
        [
            ('0', 'Europe'),
            ('1', 'America'),
            ('2', 'China'),
            ('3', 'Australia'),
            ('4', 'Israel'),
            ('5', 'Japan'),
            ('6', 'Korea'),
            ('7', 'New Zealand'),
            ('8', 'Russia'),
            ('9', 'India'),
            ('10', 'Brazil'),
            ('11', 'Philippines'),
            ('12', 'Vietnam')
        ], string="!D Reader Region", default='0')
    idreader_output_power = fields.Float(
        'Output Power (dBm)', default=20.0)
    idreader_read_time = fields.Integer(
        'Read Duration (Seconds)', default=5)

    @api.onchange('idreader_output_power')
    def onchange_idreader_output_power(self):
        warning = {}
        result = {}
        if self.idreader_output_power < 0 or self.idreader_output_power > 36:
            warning = {
                'title': _('Warning!'),
                'message': _(
                    'The output power must be between 0.0 and 36.0 dBm')
            }
            self.idreader_output_power = 20.0
        if warning:
            result['warning'] = warning
        return result

    @api.multi
    def set_idreader_region_output_power(self):
        self.ensure_one()
        if not self.proxy_ip or not self.iface_idreader:
            raise exceptions.UserError(
                _('Please define a proxy that uses the !D Reader interface'))
        action_params = {
            "url": "http://%s:8069/hw_proxy/rfid_output_power" % self.proxy_ip,
            "output_power": self.idreader_output_power * 10,
            "region": self.idreader_region,
        }

        return {
            'type': 'ir.actions.client',
            'name': 'Set OutPut Power',
            'tag': 'idreader.set_output_power',
            'params': action_params
        }
