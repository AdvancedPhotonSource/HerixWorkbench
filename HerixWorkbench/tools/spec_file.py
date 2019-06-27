#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
from spec2nexus.spec import SpecDataFile, SpecDataFileHeader
from HerixWorkbench.widgets.scan_browser import ScanBrowser

import os
# ---------------------------------------------------------------------------------------------------------------------#


class SpecFile(qtCore.QObject):

    # Slots
    reloadCounters = qtCore.pyqtSignal(object, name="reloadCounters")
    scansSelected = qtCore.pyqtSignal(list, name="scansSelected")

    def __init__(self, specPath):
        super(SpecFile, self).__init__(parent=None)
        self.specFilePath = specPath
        self.specFile = SpecDataFile(specPath)
        self.scanBrowser = ScanBrowser()
        self.scanBrowser.loadScans(self.getScans(), self)

        self.selectedScans = []

    def getSpecFilePath(self):
        return self.specFilePath

    def getSpecFileName(self):
        return os.path.split(self.specFilePath)[1]

    def getScans(self):
        return self.specFile.scans

    def getSpecLabels(self):
        return self.specFile.scans[self.selectedScans[0].scan].L

    def getScanTypes(self):
        """Gets the scan types from the spec file."""
        scanTypes = set()
        for scan in self.getScans():
            if self.isNumber(self.specFile.scans[scan].scanCmd.split()[1]) is True:
                type = self.specFile.scans[scan].scanCmd.split()[0]
            else:
                type = self.specFile.scans[scan].scanCmd.split()[0] + " " + self.specFile.scans[scan].scanCmd.split()[1]
            scanTypes.add(type)

        scanTypes = list(scanTypes)
        scanTypes.sort(key=str.lower)
        return scanTypes

    def isNumber(self, value):
        """Checks to make sure value is a number"""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def getDiamPlacements(self):
        try:
            anas_o = {}
            oData = self.specFile.scans["1"].header.O

            for i in range(len(oData)):
                oLine = oData[i]
                for j in range(len(oLine)):
                    if oLine[j].find("Ana") == 0:
                        ana = oLine[j].split("_")[0]
                        anas_o.update({str(ana): [i, j]})

            print("anas_o: ", anas_o)

            return anas_o
        except Exception as ex:
            return None

    def getAnalyzersHKLPlacements(self):
        try:
            anas_h = {}
            hData = self.specFile.scans["1"].header.H

            for i in range(len(hData)):
                hLine = hData[i]

                if hLine[0].find("T_Sample") == 0:
                    anas_h.update({'Temp': i})
                if hLine[0].find("Ana") == 0:
                    ana = hLine[0].split("_")[0]
                    anas_h.update({str(ana): i})
            print("anas_h: ", anas_h)
            return anas_h
        except Exception as ex:
            return None

    def scanSelection(self, scans):
        """Loads the selectedScans list from the scans dictionary.
        """
        print(self.getSpecFileName(), " scan selection method.")
        self.selectedScans = []  # Clears the list before adding the scans
        for scan in scans:
            self.selectedScans.append(scans[scan])

        self.scanBrowser.primaryScan = self.selectedScans[0]

        # If there is only one scan selected, it sends a
        # signal to reload the counters
        if len(self.selectedScans) == 1:
            self.reloadCounters[object].emit(self)

        self.scansSelected[list].emit(self.selectedScans)


    def loadScanBrowser(self):
        self.scanBrowser.loadScanBrowser(self.getScans())
        self.scanBrowser.scanSelected.connect(self.scanSelection)
        self.scanBrowser.scanList.setSelectionMode(qtWidgets.QAbstractItemView.SingleSelection)

    def clearScanBrowserSelection(self):
        self.scanBrowser.clear()
        self.selectedScans.clear()
        self.scanBrowser.prevSelectedScans.clear()
        self.scanBrowser.scanList.clearSelection()
