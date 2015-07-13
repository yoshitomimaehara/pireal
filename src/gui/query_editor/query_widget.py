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

from PyQt4.QtGui import (
    QDockWidget,
    QTabWidget,
    QWidget,
    QColor,
    QMessageBox
)
from PyQt4.QtCore import (
    SIGNAL,
    Qt
)
from src.gui.query_editor import editor
from src.gui.main_window import Pireal
from src.core import parser


class QueryWidget(QDockWidget):

    def __init__(self):
        super(QueryWidget, self).__init__()
        # Remove title bar widget
        title_bar = self.titleBarWidget()
        empty = QWidget()
        self.setTitleBarWidget(empty)
        del title_bar

        self.__nquery = 1
        # Tabs
        self.tab = QTabWidget()
        self.tab.setTabsClosable(True)
        self.setWidget(self.tab)

        Pireal.load_service("query_widget", self)

        # Connections
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),
                     self.removeTab)
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),
                     self._check_count)

    def resizeEvent(self, event):
        height = Pireal.get_service("pireal").height()
        height = height / 3
        self.setMinimumHeight(height)

    def _check_count(self):
        """ Hide dock if count = 0 """

        if self.tab.count() == 0:
            pireal = Pireal.get_service("pireal")
            pireal.enable_disable_query_actions(False)
            self.hide()

    def new_query(self):
        """ Add new query editor in QTabWidget """

        qeditor = editor.Editor()
        index = self.tab.addTab(qeditor,
                                self.tr("consulta_{}".format(self.__nquery)))
        self.tab.setCurrentIndex(index)
        self.__nquery += 1

        self.connect(qeditor, SIGNAL("modificationChanged(bool)"),
                     self.__editor_modified)

    def execute_queries(self):
        import re
        # Editor instance
        editor = self.tab.currentWidget()
        # Text
        text = editor.toPlainText()
        # Ignore comments
        table = Pireal.get_service("container").table_widget
        for line in text.splitlines():
            if line.startswith('--'):
                continue
            parts = line.split('=', 1)
            parts[0] = parts[0].strip()
            if re.match(r'^[_a-zA-Z]+[_a-zA-Z0-9]*$', parts[0]):
                relation_name, line = parts
            else:
                relation_name = 'rel'
            expression = parser.convert_to_python(line.strip())
            rel = eval(expression, table.relations)
            table.add_new_table(rel, relation_name)
            table.relations[relation_name] = rel

    def __editor_modified(self, modified):
        """ This function changes the text color of the tab when
        it receives the signal *modificationChanged(bool)*

        :param modified: Boolean value sent by the signal
        """

        if modified:
            self.tab.tabBar().setTabTextColor(self.tab.currentIndex(),
                                              QColor(Qt.red))
        else:
            self.tab.tabBar().setTabTextColor(self.tab.currentIndex(),
                                              QColor(Qt.black))
        editor = self.tab.currentWidget()
        editor.modified = modified

    def removeTab(self, index):
        # Current editor instance
        editor = self.tab.currentWidget()
        if editor.modified:
            flags = QMessageBox.Yes
            flags |= QMessageBox.No
            flags |= QMessageBox.Cancel
            r = QMessageBox.information(self, self.tr("Modified"),
                                        self.tr("lalalal"), flags)
            if r == QMessageBox.Cancel:
                return
            if r == QMessageBox.Yes:
                print("Guardando")
            else:
                print("Saliendo...")
        self.tab.removeTab(index)

query_widget = QueryWidget()
