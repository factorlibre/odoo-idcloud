# -*- coding: utf-8 -*-
# © 2018 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'PoS: !D Reader RFID Tag Reader integration: Return Operations',
    'version': '10.0.1.0.0',
    'depends': [
        'pos_idreader',
        'pos_order_return_complete'
    ],
    'category': 'Sales Management',
    'author': 'FactorLibre',
    'license': 'AGPL-3',
    'website': 'http://www.factorlibre.com',
    'data': [
        'templates/assets.xml'
    ],
    'qweb': ['static/src/xml/pos_idreader_return.xml'],
    'installable': True,
    'application': False,
    'auto_install': True
}
