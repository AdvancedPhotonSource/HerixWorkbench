#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals

import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
from HerixWorkbench.tools.spec_file import SpecFile
# ----------------------------------------End of Imports---------------------------------------------------------------#


class SpecFileList(qtWidgets.QWidget):
    """List that displays the spec files loaded to the program. Uses a QListWidget to list out checkboxes
    that when selected, load the scans into the scan browser."""

    # Signals
    specFileSelected = qtCore.pyqtSignal(object, name="specFileSelected")
    specFileRemoved = qtCore.pyqtSignal(object, name="specFileRemoved")
    loadCounters = qtCore.pyqtSignal(object, name="loadCounters")
    update_plot = qtCore.pyqtSignal(name="update_plot")

    def __init__(self, parent=None):
        super(SpecFileList, self).__init__(parent)
        self.specFileList = qtWidgets.QListWidget()
        hLayout = qtWidgets.QHBoxLayout()
        self.specFileList.setSelectionMode(qtWidgets.QAbstractItemView.NoSelection)
        self.specFileList.setFocusPolicy(qtCore.Qt.NoFocus)
        self.specFileList.itemChanged.connect(self.specFileChanged)
        hLayout.addWidget(self.specFileList)
        self.setLayout(hLayout)

        self.specFiles = []
        self.selectedSpecFiles = []
        self.selectedScans = []

    def addSpecFile(self, path):
        """Loads the spec file into the SpecFileList. If there's
         no file selected, it will select the spec file
        :param path: path of spec file
        """
        specFile = SpecFile(path)
        specFile.reloadCounters.connect(self.reload_counters)
        specFile.scansSelected.connect(self.scans_selected)
        item = qtWidgets.QListWidgetItem()
        item.setFlags(item.flags() | qtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(qtCore.Qt.Unchecked)
        item.setText(specFile.getSpecFileName())
        self.specFiles.append(specFile)
        self.specFileList.addItem(item)

        # First spec file opened gets loaded
        if len(self.selectedSpecFiles) == 0:
            item.setCheckState(qtCore.Qt.Checked)

    def specFileChanged(self, item):
        """ Method gets activated when an item changes,
        it returns the changed spec file through the appropriate
        signal
        :param item: changed item
        """
        specFile = self.specFiles[self.specFileList.row(item)]
        if item.checkState() == 2:
            self.selectedSpecFiles.append(specFile)
            self.specFileSelected[object].emit(self.specFiles[self.specFileList.row(item)])
        else:
            self.selectedSpecFiles.remove(specFile)
            specFile.clearScanBrowserSelection()
            self.specFileRemoved[object].emit(specFile)

    def reload_counters(self, specFile):
        """Sends signal to herix_workbench_window to reload the counters.
        WIll only send if a new scan is selected from the primary spec file
        """
        if self.selectedSpecFiles[0] == specFile:
            self.loadCounters[object].emit(specFile)

    def scans_selected(self):
        print("Set scans, spec file list")

        self.selectedScans = []
        for specFile in self.selectedSpecFiles:
            scans = specFile.selectedScans
            for scan in scans:
                self.selectedScans.append(scan)

        for scan in self.selectedScans:
            print(scan.scan, scan.getSpecFileName())

        self.update_plot.emit()
