# -*- coding: utf-8 -*-
# © 2018 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'PoS: !D Reader RFID Tag Reader integration',
    'version': '10.0.1.0.0',
    'depends': [
        'point_of_sale',
        'web'
    ],
    'category': 'Sales Management',
    'author': 'FactorLibre',
    'license': 'AGPL-3',
    'website': 'http://www.factorlibre.com',
    'data': [
        'templates/assets.xml',
        'views/pos_config_view.xml'
    ],
    'qweb': ['static/src/xml/pos_idreader.xml'],
    'installable': True,
    'application': False
}
