#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
from PyQt5.QtCore import *
from spec2nexus.spec import SpecDataFile, SpecDataFileHeader

import os
# ---------------------------------------------------------------------------------------------------------------------#

class SpecFile(QObject):

    def __init__(self, specPath):
        super(SpecFile, self).__init__(parent=None)
        self.specFilePath = specPath
        self.specFile = SpecDataFile(specPath)
        self.scanBrowserIndex = None
        print(self.specFilePath)

    def getSpecFilePath(self):
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

    def getScanBrowserIndex(self):
        return self.scanBrowserIndex

    def setScanBrowserIndex(self, indx):
        self.scanBrowserIndex = indx
