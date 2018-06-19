
"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# ----------------------------------------End of Imports---------------------------------------------------------------#

class SpecFileSelectionList(QWidget):
    """List that displays the spec files loaded to the program. Uses a QListWidget to list out checkboxes
    that when selected, load the scans into the scan browser."""

    # Signals
    specFileChanged = pyqtSignal(int, name="specFileChanged")
    noSpecFileSelected = pyqtSignal(name="noSpecFileSelected")

    def __init__(self, parent=None):
        super(SpecFileSelectionList, self).__init__(parent)
        self.specFileList = QListWidget()
        hLayout = QHBoxLayout()
        self.specFileList.setSelectionMode(QAbstractItemView.NoSelection)
        self.specFileList.setFocusPolicy(Qt.NoFocus)
        self.specFileList.itemChanged.connect(self.specFileSelected)
        hLayout.addWidget(self.specFileList)
        self.setLayout(hLayout)

        self.prevSelectedFile = None
        self.specFileArray = []

    def addSpecFile(self, path, fileName):
        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        item.setText(fileName)
        self.specFileArray.append(path)
        self.specFileList.addItem(item)

        if self.specFileList.count() == 1:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

    def specFileSelected(self, item):
        print("Spec FIle changed")
        if self.prevSelectedFile is None:
            self.prevSelectedFile = item
        elif self.prevSelectedFile == item:
            print(item.checkState())
            if item.checkState() == 2:
                print("I'm in and checked")
                self.prevSelectedFile = item
                self.specFileChanged[int].emit(self.specFileList.row(item))
            else:
                print("No spec")
                self.noSpecFileSelected.emit()
        else:
            self.prevSelectedFile.setCheckState(Qt.Unchecked)
            self.prevSelectedFile = item
            self.specFileChanged[int].emit(self.specFileList.row(item))

