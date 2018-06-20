#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
from spec2nexus.spec import SpecDataFile, SpecDataFileHeader
from PyQt5.QtWidgets import *
import os
# ----------------------------------------End of Imports---------------------------------------------------------------#


class SpecData:
    """Gets and sets information that is located in the spec file. """

    def __init__(self):
        self.specFile = None
        self.specFileHeader = None
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
        self.specFileHeader = SpecDataFileHeader(open(filePath))
        self.specOpen = True

    def getScans(self):
        """Gets scan from the spec file
        :return: scans
        """
        return self.specFile.scans

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


    def scanSelection(self, scans):
        """This method is called when a PVvalue is selected or unselected. It updates
        which scans are selected."""
        print(self.selectedScans)
        self.selectedScans = scans
        if len(self.selectedScans) > 0:
            self.scanHasBeenSelected = True
            self.getDetectorInfoDictionary()

    def getSpecDetectorData(self, scan, detector):
        if detector == None:
            return []
        else:
            return self.specFile.scans[str(scan)].data[detector]

    def getPlotLegendInfo(self, detector):
        try:
            detInfo = self.scanInfo[detector]
            h = detInfo[0]
            k = detInfo[1]
            l = detInfo[2]
            diam = detInfo[3]
            return h, k, l, diam
        except Exception as ex:
            QMessageBox.warning(None, "HKL error", "There was an error retrieving hkl for detector " + detector + "."
                                "\n\nException: " + str(ex))
            return 0,0,0

    def specShortName(self, filePath):
        return os.path.split(filePath)[1]

    def getDetectorInfoDictionary(self):
        """This method creates a dictionary with information for each detector in a particular scan.
        :return:
        """
        #  I might need to make some changes to take into account the selection of other scans
        try:
            vData = self.specFile.scans[str(self.selectedScans[0])].V
            anas_d = self.getAnas_diam()
            self.scanInfo.update({"Temp": vData[2]})
            self.scanInfo.update({"PIN-C": [0, 0, 0, 100]})

            # Gets the hkl for each analyzer, which are located in #V4-#V12
            for i in range(4, 13):
                info = vData[i]
                diam = 100
                for d in anas_d:
                    if d == "Anal"+str(i-3):
                        diam = anas_d[d]
                info.append(diam)

                self.scanInfo.update({"Ana"+str(i-3): info})

            print(vData)
            print(self.scanInfo)
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

    def getAnas_diam(self):
        """This method gets the Ana detectors diam from the spec file. It finds them using the #O from the header,
        and finding their value under the scan #P.
        :return: dictionary with detectors and their diam
        """
        try:
            anas_d = {}
            anas_o = {}
            oData = self.specFile.scans[str(self.selectedScans[0])].header.O
            pData = self.specFile.scans[str(self.selectedScans[0])].P

            for i in range(len(oData)):
                oLine = oData[i]
                for j in range(len(oLine)):
                    if oLine[j].find("Anal") == 0:
                        ana = oLine[j].split("_")[0]
                        anas_o.update({str(ana): [i, j]})

            for o in anas_o:
                row, col = anas_o[o]
                pRow = pData[row].split()
                p = pRow[col]
                anas_d.update({o : p})

            return anas_d
        except Exception as ex:
            QMessageBox.warning(None, "Error", "There was an error retrieving the anal_diam \n\nError: " + str(ex))
            return None




