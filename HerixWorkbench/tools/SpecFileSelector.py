#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from HerixWorkbench.source.specFile import SpecFile
# ----------------------------------------End of Imports---------------------------------------------------------------#

class SpecFileSelectionList(QWidget):
    """List that displays the spec files loaded to the program. Uses a QListWidget to list out checkboxes
    that when selected, load the scans into the scan browser."""

    # Signals
    specFileChanged = pyqtSignal(int, name="specFileChanged")
    noSpecFileSelected = pyqtSignal(int, name="noSpecFileSelected")

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
        self.selectedSpecFile = []

    def addSpecFile(self, path):
        specFile = SpecFile(path)
        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        item.setText(specFile.getSpecFileName())
        self.specFileArray.append(specFile)
        self.specFileList.addItem(item)

        if self.specFileList.count() == 1:
            item.setCheckState(Qt.Checked)

    def specFileSelected(self, item):
        print("Item has been checked: " + str(self.specFileList.row(item)))
        print(self.selectedSpecFile)
        if item.checkState() == 2:
            self.selectedSpecFile.append(self.specFileList.row(item))
            self.specFileChanged[int].emit(self.specFileList.row(item))
        else:
            for i in range(len(self.selectedSpecFile)):
                if self.selectedSpecFile[i] == self.specFileList.row(item):
                    self.selectedSpecFile.pop(i)
                    break
            self.noSpecFileSelected[int].emit(self.specFileList.row(item))




