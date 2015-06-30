# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of Pireal.
#
# Pireal is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Pireal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pireal; If not, see <http://www.gnu.org/licenses/>.

"""
Default in Spanish
"""

from collections import OrderedDict
from PyQt4.QtGui import QApplication

tr = QApplication.translate


MENU = OrderedDict()


# Menu File
MENU['file'] = {
    'name': tr("Pireal", "&Archivo"),
    'items': [{
        'name': tr("Pireal", "Nueva Base de Datos"),
        'slot': "actions:create_data_base"}]
    }