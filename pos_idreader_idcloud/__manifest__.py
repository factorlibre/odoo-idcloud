# -*- coding: utf-8 -*-
# © 2018 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'PoS: !D Reader - !D Cloud Integration',
    'version': '10.0.1.0.0',
    'depends': [
        'pos_idreader',
        'pos_idreader_return',
        'connector_idcloud_rfid'
    ],
    'category': 'Sales Management',
    'author': 'FactorLibre',
    'license': 'AGPL-3',
    'website': 'http://www.factorlibre.com',
    'data': [
        'templates/assets.xml'
    ],
    'qweb': [],
    'installable': True,
    'auto_install': True,
    'application': False,
    'sequence': 100
}
