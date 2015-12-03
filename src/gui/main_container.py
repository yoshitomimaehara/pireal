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

#import os

from PyQt5.QtWidgets import (
    QSplitter,
    #QFileDialog,
    #QMessageBox
)
from PyQt5.QtCore import Qt

#from src.gui.main_window import Pireal
from src.gui import (
    #database_widget
    table_widget,
    list_widget,
    table
)
from src.gui.query_container import query_container
#from src import translations as tr
from src.core import (
    relation,
    #pfile,
    #settings,
    #file_manager
)
    #table_widget,
    #lateral_widget
#)


class MainContainer(QSplitter):

    def __init__(self, orientation=Qt.Vertical):
        QSplitter.__init__(self, orientation)

        self._hsplitter = QSplitter(Qt.Horizontal)

        self.lateral_widget = list_widget.LateralWidget()
        self._hsplitter.addWidget(self.lateral_widget)
        self.table_widget = table_widget.TableWidget()
        self._hsplitter.addWidget(self.table_widget)

        self.addWidget(self._hsplitter)

        self.query_container = query_container.QueryContainer()
        self.addWidget(self.query_container)

        self.lateral_widget.currentRowChanged[int].connect(
            lambda i: self.table_widget.stacked.setCurrentIndex(i))
        #self.db_widget = database_widget.DBWidget()
        #self.addWidget(self.db_widget)

        #self.query_tab_container = query_container.QueryTabContainer()
        #self.query_tab_container.hide()
        #self.addWidget(self.query_tab_container)

        #self.__ndatabase, self.__nquery, self.__nrelation = 1, 1, 1

        # To remember the last folder
        #if settings.PSettings.LAST_OPEN_FOLDER:
            #self.__last_open_folder = settings.PSettings.LAST_OPEN_FOLDER
        #else:
            #self.__last_open_folder = None

        self.setSizes([1, 1])

        # Load service
        #Pireal.load_service("main", self)

    #def open_file(self, filename=''):
        #if self.__last_open_folder is None:
            #directory = os.path.expanduser("~")
        #else:
            #directory = self.__last_open_folder

        #filename = QFileDialog.getOpenFileName(self, tr.TR_CONTAINER_OPEN_FILE,
                                               #directory, settings.DBFILE)[0]
        #if not filename:
            #return

        ## Save folder
        #self.__last_open_folder = file_manager.get_path(filename)

        #extension = file_manager.get_extension(filename)
        #if extension == '.pqf':
            #central = Pireal.get_service("central")
            #if not central.created:
                #QMessageBox.information(central, "Information",
                                        #"First create or open a database")
                #return
            ## Query file
            #self.new_query(filename)
        #else:
            ## Database file
            #self.create_database(filename)

    #def get_last_open_folder(self):
        #return self.__last_open_folder

    #def create_database(self, filename=''):
        #""" This function opens or creates a database """

        #central = Pireal.get_service("central")
        #if central.created:
            #QMessageBox.critical(self, "Error", tr.TR_CONTAINER_ERROR_DB)
            #return
        #central.add_main_container()
        ## Pireal File
        #ffile = pfile.PFile(filename)
        #if filename:
            #try:
                #data = ffile.read()
            #except Exception as reason:
                #QMessageBox.critical(self, "Error", reason.__str__())
                #return
            #db_name = ffile.name
            ##self.db_widget.table_widget.add_data_base(data)
            #self.table_widget.add_data_base(data)
        #else:
            #db_name = "database_{}.pdb".format(self.__ndatabase)
        #pireal = Pireal.get_service("pireal")
        ## Title
        #pireal.change_title(db_name)
        ## Enable QAction's
        #pireal.enable_disable_db_actions()
        #central.created = True
        #self.__ndatabase += 1
        # Add to recent databases
        #self.__add_to_recent(ffile.filename)

    def create_database(self, data):
        rel = None
        for part in data.split('@'):
            for e, line in enumerate(part.splitlines()):
                # Remove whitespaces
                line = ','.join(list(map(str.strip, line.split(','))))
                if e == 0:
                    if line.endswith(','):
                        line = line[:-1]
                    name = line.split(':')[0]
                    rel = relation.Relation()
                    rel.fields = line.split(':')[-1].split(',')
                else:
                    rel.insert(line.split(','))
            if rel is not None:
                ptable = table.Table()
                ptable.setColumnCount(len(rel.fields))
                ptable.setHorizontalHeaderLabels(rel.fields)
                self.table_widget.add_relation(name, rel)

                for row in rel.content:
                    nrow = ptable.rowCount()
                    ptable.insertRow(nrow)
                    for col, text in enumerate(row):
                        item = table.Item()
                        item.setText(text)
                        ptable.setItem(nrow, col, item)

                self.table_widget.stacked.addWidget(ptable)
                self.lateral_widget.add_item(name, nrow)
    #def __add_to_recent(self, filename):
        #files = settings.get_setting('recentDB', [])
        #if filename not in files:
            #files.insert(0, filename)
            #del files[settings.PSettings.MAX_RECENT_FILES:]
            #settings.set_setting('recentDB', files)

    #def get_recent_db(self):
        #return settings.PSettings.RECENT_DB

    #def close_database(self):
        #pass

    #def create_new_relation(self):
        #from src.gui.dialogs import new_relation_dialog
        #d = new_relation_dialog.NewRelationDialog()
        #d.show()

    #def _change_state_actions(self, value):
        #qactions = [
            #'undo_action',
            #'redo_action',
            #'copy_action',
            #'cut_action',
            #'paste_action',
        #]
        #for qaction in qactions:
            #Pireal.get_action(qaction).setEnabled(value)

    #def new_query(self, filename=''):
        #self.query_container.add_tab()
        #qcontainer = query_container.QueryContainer()
        #qcontainer.editorFocused.connect(self._change_state_actions)
        #qcontainer.editorModified.connect(self._editor_modified)

        #if not filename:
            #ffile = pfile.PFile()
            #filename = "New_query_{}.qpf".format(self.__nquery)
            #ffile.filename = filename
            #self.__nquery += 1
        #else:
            #ffile = pfile.PFile(filename)
            #qcontainer.add_editor_text(ffile.read())

        #qcontainer.set_pfile(ffile)

        #if not self.query_tab_container.isVisible():
            #self.query_tab_container.show()

        #pireal = Pireal.get_service("pireal")
        #pireal.enable_disable_query_actions()

        #index = self._add_query_tab(qcontainer, ffile.name)
        #self.query_tab_container.setTabToolTip(index, ffile.filename)

        #self.setSizes([(self.height() / 5) * 2, 1])

    #def _add_query_tab(self, widget, title):
        #return self.query_tab_container.add_tab(widget, title)

    #def _editor_modified(self, modified):
        #self.query_tab_container.tab_modified(modified)
        #weditor = self.query_tab_container.currentWidget().editor()
        #weditor.modified = True

    #def execute_queries(self):
        #self.query_container.execute_queries()

    def showEvent(self, event):
        QSplitter.showEvent(self, event)
        self._hsplitter.setSizes([1, self._hsplitter.width() / 3])

#main = MainContainer()
