#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox

import os
# ---------------------------------------------------------------------------------------------------------------------#


class Scan(QObject):

    def __init__(self, scan, specFile):
        super(Scan, self).__init__(parent=None)
        self.scan = scan
        self.specFile = specFile
        self.specDataFile = self.specFile.specFile.scans[self.scan]
        self.scanDetectorInfo = {}
        self.createDetectorInfoDictionary()

    def getSpecDetectorData(self, detector):
        if detector == None:
            return []
        else:
            try:
                return self.specDataFile.data[detector]
            except Exception as ex:
                QMessageBox.warning(None, "Error", "There was an error retrieving the counter data from the spec file. "
                                                   " \n\nError: " + str(ex))
                return 0

    def getAnas_diam(self):
        """This method gets the Ana detectors diam from the spec file. It finds them using the #O from the header,
        and finding their value under the scan #P.
        :return: dictionary with detectors and their diam
        """
        try:
            anas_d = {}
            anas_o = self.specFile.getDiamPlacements()
            pData = self.specDataFile.P

            for o in anas_o:
                row, col = anas_o[o]
                pRow = pData[row].split()
                p = pRow[col]
                p = round(float(p), 2)
                anas_d.update({o: p})

            return anas_d
        except Exception as ex:
            QMessageBox.warning(None, "Error", "There was an error retrieving the anal_diam \n\nError: " + str(ex))
            return None

    def getTempHKLInfo(self):
        """This method gets the Ana detectors diam from the spec file. It finds them using the #O from the header,
        and finding their value under the scan #P.
        :return: dictionary with detectors and their diam
        """
        try:
            scanInfo = {}
            hInfo = self.specFile.getAnalyzersHKLPlacements()
            vData = self.specDataFile.V

            for h in hInfo:
                row = hInfo[h]
                data = vData[row]
                for i in range(len(data)):
                    data[i] = float(round(float(data[i]), 3))
                scanInfo.update({h: data})

            print("Spec Info")
            print(scanInfo)
            return scanInfo
        except Exception as ex:
            QMessageBox.warning(None, "Error", "There was an error retrieving the anal_diam \n\nError: " + str(ex))
            return None

    def createDetectorInfoDictionary(self):
        """This method creates a dictionary with information for each detector in a particular scan.
        :return:
        """
        try:
            diamData = self.getAnas_diam()
            tempHKLInfo = self.getTempHKLInfo()
            data = []
            diam = 0

            self.scanDetectorInfo.update({"Temp": tempHKLInfo["Temp"]})
            self.scanDetectorInfo.update({"PIN-C": [0, 0, 0, 100]})

            for i in range(1, 10):
                data = tempHKLInfo["Analyzer" + str(i)]
                diam = 100
                for d in diamData:
                    if d == "Anal" + str(i):
                        diam = diamData[d]
                data.append(diam)
                self.scanDetectorInfo.update({"Ana" + str(i): data})
        except Exception as ex:
            QMessageBox.warning(None, "Error", "There was an error retrieving the HKL for the ANA detectors and"
                                               " the temperature from the spec file."
                                                   "\n\n Exception: " + str(ex))

    def getDetectorXAxis(self):
        try:
            axis = self.specDataFile.L[0]
            x = self.specDataFile.data[axis]
            return x, axis
        except Exception as ex:
            QMessageBox.warning(None, "Error", "There was an error retrieving the x-axis for scan " + self.scan + "." +
                                "\n\n Exception: " + str(ex))
            return 0, None

    def getScanNumber(self):
        return self.scan

    def getSpecFileName(self):
        return self.specFile.getSpecFileName()

    def getPlotLegendInfo(self, detector):
        try:
            detInfo = self.scanDetectorInfo[detector]
            h = detInfo[0]
            k = detInfo[1]
            l = detInfo[2]
            diam = detInfo[3]
            return h, k, l, diam
        except Exception as ex:
            QMessageBox.warning(None, "HKL error", "There was an error retrieving hkl for detector " + detector +
                                ". \n\nException: " + str(ex))
            return 0, 0, 0