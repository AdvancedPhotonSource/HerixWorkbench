#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidget
from spec2nexus.spec import SpecDataFile, SpecDataFileHeader
from HerixWorkbench.source.scan import Scan

import os
# ---------------------------------------------------------------------------------------------------------------------#

class SpecFile(qtCore.QObject):
    """Spec file object. Gets information for the spec file loaded in the program"""

    def __init__(self, specPath):
        super(SpecFile, self).__init__(parent=None)
        self.specFilePath = specPath
        self.specFile = SpecDataFile(specPath)
        self.scanBrowserIndex = None
        self.getAnalyzersHKLPlacements()

        self.selectedScans = []

    def getSpecFilePath(self):
        """:return: gets the path of the spec file
        """
        return self.specFilePath

    def getSpecFileName(self):
        return os.path.split(self.specFilePath)[1]

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
        try:
            float(value)
            return True
        except ValueError:
            return False

    def getScans(self):
        """Gets scan from the spec file
        :return: scans
        """
        return self.specFile.scans

    def getDiamPlacements(self):
        try:
            anas_o = {}
            oData = self.specFile.scans["1"].header.O

            for i in range(len(oData)):
                oLine = oData[i]
                for j in range(len(oLine)):
                    if oLine[j].find("Anal") == 0:
                        ana = oLine[j].split("_")[0]
                        anas_o.update({str(ana): [i, j]})

            return anas_o
        except Exception as ex:
            qtWidget.QMessageBox.warning(None, "Error", "There was an error retrieving the anal_diam \n\nError: "
                                         + str(ex))
            return None

    def getAnalyzersHKLPlacements(self):
        try:
            anas_h = {}
            hData = self.specFile.scans["1"].header.H

            for i in range(len(hData)):
                hLine = hData[i]

                if hLine[0].find("T_Sample") == 0:
                    anas_h.update({'Temp': i})
                if hLine[0].find("Anal") == 0:
                    ana = hLine[0].split("_")[0]
                    anas_h.update({str(ana): i})

            return anas_h
        except Exception as ex:
            qtWidget.QMessageBox.warning(None, "Error", "There was an error retrieving the HKL placements. \n\nError: " + str(ex))
            return None

    def scanSelection(self, scans):
        self.selectedScans = []
        for s in scans:
            scan = Scan(s, self)
            print(scan.getScanNumber())
            self.selectedScans.append(scan)

    def getSpecLabels(self):
        print("Selected Scans: ", len(self.selectedScans))
        print(self.selectedScans)
        if len(self.selectedScans) > 0:
            return self.specFile.scans[str(self.selectedScans[0].scan)].L
        else:
            qtWidget.QMessageBox.warning(None, "Error",
                                         "You must select a scan for the counters to display.")
            return ["No", "Scan", "Selected"]

