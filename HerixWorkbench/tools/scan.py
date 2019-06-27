#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
import PyQt5.QtCore as qtCore
from PyQt5.QtWidgets import QMessageBox, QDoubleSpinBox

import os
# ---------------------------------------------------------------------------------------------------------------------#


class Scan(qtCore.QObject):
    """Scan object class, gets information for a particular scan
    """
    # Slots
    plotShifterChanged = qtCore.pyqtSignal(object, name="plotShifterChanged")

    def __init__(self, scan, specFile):
        super(Scan, self).__init__(parent=None)
        self.scan = scan
        self.specFile = specFile
        self.specDataFile = self.specFile.specFile.scans[self.scan]
        self.scanDetectorInfo = {}
        self.tableRow = -1
        self.temp1 = 0
        self.temp2 = 0

        self.plotShifter = None
        self.createdInfoDic = False

    def getScanNumber(self):
        return self.scan

    def getSpecFileName(self):
        return self.specFile.getSpecFileName()

    def getTemp(self):
        return self.temp1, self.temp2

    def getSpecDetectorData(self, detector):
        try:
            return self.specDataFile.data[detector]
        except Exception as ex:
            return None

    def getShifterVal(self):
        """ Returns the value of the plotShifter
        :return: shifter value
        """
        return self.plotShifter.Value()

    def shiftValueChanged(self, val):
        self.plotShifterChanged[object].emit(self)

    def getShifter(self):
        return self.plotShifter

    def getDetectorXAxis(self):
        try:
            axis = self.specDataFile.L[0]
            x = self.specDataFile.data[axis]
            return x, axis
        except Exception as ex:
            return None, None

    def getAnas_diam(self):
        """This method gets the Ana detectors diam from the spec file. It finds them using their position in
         #O from the header, and finding their value under the scan #P.
        :return: dictionary with detectors and their diam
        """
        try:
            anas_d = {}
            anas_o = self.specFile.getDiamPlacements()

            if anas_d is None:
                return None

            pData = self.specDataFile.P

            for o in anas_o:
                row, col = anas_o[o]
                pRow = pData[row].split()
                p = pRow[col]
                p = round(float(p), 2)
                anas_d.update({o: p})
            print("anas_d: ", anas_d)
            return anas_d
        except Exception as ex:
            return None

    def getTempHKLInfo(self):
        """This method gets the Ana detectors diam from the spec file. It finds them using the #O from the header,
        and finding their value under the scan #P.
        :return: dictionary with detectors and their diam
        """
        try:
            scanInfo = {}
            hInfo = self.specFile.getAnalyzersHKLPlacements()
            if hInfo is None:
                return None
            vData = self.specDataFile.V

            for h in hInfo:
                row = hInfo[h]
                data = vData[row]
                for i in range(len(data)):
                    data[i] = float(round(float(data[i]), 3))
                scanInfo.update({h: data})

            print("scanInfo: ", scanInfo)
            return scanInfo
        except Exception as ex:
            return None

    def createDetectorInfoDictionary(self):
        """This method creates a dictionary with information for each detector in a particular scan.
        :return:
        """
        try:
            if self.createdInfoDic is False:
                self.createdInfoDic = True
                diamData = self.getAnas_diam()
                tempHKLInfo = self.getTempHKLInfo()
                data = []
                diam = 0

                self.temp1, self.temp2 = tempHKLInfo["Temp"]

                for i in range(1, 10):
                    data = tempHKLInfo["Analyzer" + str(i)]
                    diam = 100
                    for d in diamData:
                        if d == "Ana" + str(i):
                            diam = diamData[d]
                    data.append(diam)
                    self.scanDetectorInfo.update({"Ana" + str(i): data})
                print("Scan Detector Info: " ,self.scanDetectorInfo)
        except Exception as ex:
            self.scanDetectorInfo = None

    def getPlotLegendInfo(self, detector):
        try:
            self.createDetectorInfoDictionary()
            if self.scanDetectorInfo is None:
                return "N/A", "N/A", "N/A", "N/A"

            detInfo = self.scanDetectorInfo[detector]
            h = detInfo[0]
            k = detInfo[1]
            l = detInfo[2]
            diam = detInfo[3]
            return h, k, l, diam
        except Exception as ex:
            return "N/A", "N/A", "N/A", "N/A"
