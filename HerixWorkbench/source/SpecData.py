#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
from spec2nexus.spec import SpecDataFile
import os
# ----------------------------------------End of Imports---------------------------------------------------------------#


class SpecData:
    """Gets and sets information that is located in the spec file. """

    def __init__(self):
        self.specFile = None
        self.selectedScans = []
        self.specOpen = False
        self.specFileName = None

    def loadSpecFile(self, fileName):
        self.specFileName = fileName
        self.specFile = SpecDataFile(fileName)
        self.specOpen = True

    def getScans(self):
        return self.specFile.scans

    def getScanTypes(self):
        """Gets the scan types from the spec file."""
        scanTypes = set()
        for scan in self.getScans():
            scanTypes.add(self.specFile.scans[scan].scanCmd.split()[0])

        scanTypes = list(scanTypes)
        scanTypes.sort(key=str.lower)
        return scanTypes

    def scanSelection(self, scans):
        """This method is called when a PVvalue is selected or unselected. It updates
        which scans are selected."""
        self.selectedScans = scans

    def getSpecDetectorData(self, detectors):
        scanData = {}
        if len(detectors) == 0:
            return scanData
        else:
            for detector in detectors:
                scanData.update({detector: self.specFile.scans[str(self.selectedScans[0])].data[detector]})

            return scanData

    def gethkl(self):
        pass

    def specShortName(self):
        return os.path.split(self.specFileName)[1]


