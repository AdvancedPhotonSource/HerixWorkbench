#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
from spec2nexus.spec import SpecDataFile
from PyQt5.QtWidgets import *
import os
# ----------------------------------------End of Imports---------------------------------------------------------------#


class SpecData:
    """Gets and sets information that is located in the spec file. """

    def __init__(self):
        self.specFile = None
        self.selectedScans = []
        self.specOpen = False
        self.specFileName = None
        self.scanHasBeenSelected = False
        self.scanInfo = {}

    def loadSpecFile(self, filePath):
        """This methods loads the file into spec2nexus
        :param filePath:
        """
        self.specFilePath = filePath
        self.specFile = SpecDataFile(filePath)
        self.specOpen = True

    def getScans(self):
        """Gets scan from the spec file
        :return: scans
        """
        return self.specFile.scans

    def getScanTypes(self):
        """Gets the scan types from the spec file."""
        scanTypes = set()
        print("SCAN TYPES")
        for scan in self.getScans():
            type = self.specFile.scans[scan].scanCmd.split()[0] + " " + self.specFile.scans[scan].scanCmd.split()[1]
            scanTypes.add(type)
            print(self.specFile.scans[scan].scanCmd.split())

        scanTypes = list(scanTypes)
        scanTypes.sort(key=str.lower)
        return scanTypes

    def scanSelection(self, scans):
        """This method is called when a PVvalue is selected or unselected. It updates
        which scans are selected."""
        print(self.selectedScans)
        self.selectedScans = scans
        if len(self.selectedScans) > 0:
            self.scanHasBeenSelected = True
            self.getAnaHKLTempDictionary()

    def getSpecDetectorData(self, scan, detector):
        if detector == None:
            return []
        else:
            return self.specFile.scans[str(scan)].data[detector]

    def getHKL(self, detector):
        try:
            detInfo = self.scanInfo[detector]
            h = detInfo[0]
            k = detInfo[1]
            l = detInfo[2]
            return h, k, l
        except Exception as ex:
            QMessageBox.warning(None, "HKL error", "There was an error retrieving hkl for detector " + detector + "."
                                "\n\nException: " + str(ex))
            return 0,0,0

    def specShortName(self, filePath):
        return os.path.split(filePath)[1]

    def getAnaHKLTempDictionary(self):
        try:
            rawData = self.specFile.scans[str(self.selectedScans[0])].raw
            splitH0 = rawData.split('#V0')
            splitN = splitH0[1].split("#N")
            vLines = splitN[0].splitlines()

            self.scanInfo.update({"Temp": vLines[2].split("#V2")[1].strip()})

            for i in range(4,13):
                v = vLines[i].split('#V' + str(i))
                v = v[1].strip()
                self.scanInfo.update({"Ana"+str(i-3): v.split()})
            #print(self.scanInfo)
        except Exception as ex:
            QMessageBox.warning(None, "Error", "There was an error retrieving the HKL for the ANA detectors and"
                                               " the temperature from the spec file."
                                                   "\n\n Exception: " + str(ex))

    def getDetectorXAxis(self, scan):
        try:
            axis = self.specFile.scans[scan].L[0]
            x = self.specFile.scans[scan].data[axis]
            return x, axis
        except Exception as ex:
            QMessageBox.warning(None, "Error", "There was an error retrieving the x-axis for scan " + scan + "." +
                                               "\n\n Exception: " + str(ex))
            return 0, None




