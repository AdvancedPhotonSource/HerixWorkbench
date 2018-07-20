#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from HerixWorkbench.tools.scanDataSelector import ScanDataSelector
from HerixWorkbench.tools.specDataSelector import SpecDataSelector
from specguiutils.scantypeselector import ScanTypeSelector
from HerixWorkbench.source.PlotWidget import PlotWidget
from HerixWorkbench.tools.SpecFileSelector import SpecFileSelectionList
# ---------------------------------------------------------------------------------------------------------------------#


class HerixWorkbenchWindow(QMainWindow):
    """Main window class"""
    def __init__(self, parent=None):
        super(HerixWorkbenchWindow, self).__init__(parent)
        self.setGeometry(50, 50, 1500, 800)
        self.setWindowTitle("Herix Workbench")
        self.setMinimumSize(1000, 650)
        self.windowSplitter = QSplitter()
        self.PlotWidget = PlotWidget()  # Class
        self.plotWidget = self.PlotWidget.plotWidget  # Widget

        self.selectedDetectors = []
        self.selectedScans = []
        self.scans = None

        self.CreateSpecDataSplitter()
        self.createMenuBar()
        self.windowSplitter.addWidget(self.specSplitter)
        self.windowSplitter.addWidget(self.plotWidget)
        self.setCentralWidget(self.windowSplitter)

    def CreateSpecDataSplitter(self):
        """Creates the QSplitter with the spec and detector widgets."""
        self.specSplitter = QSplitter()
        self.specSplitter.setFixedWidth(400)
        self.specSplitter.setOrientation(Qt.Vertical)
        self.createPlotTypeComboBox()

        self.specFileList = SpecFileSelectionList()
        self.specFileList.specFileChanged.connect(self.newSpecFileSelected)
        self.specFileList.noSpecFileSelected.connect(self.noSpecFileSelected)
        self.scanDataSelector = ScanDataSelector()
        self.scanTypeSelector = ScanTypeSelector()
        self.scanTypeSelector.scanTypeChanged.connect(self.filterScansByType)
        self.specDataSelector = SpecDataSelector()
        self.specDataSelector.detectorsSelected.connect(self.setSelectedPlotDetectors)

        self.specSplitter.addWidget(self.specFileList)
        self.specSplitter.addWidget(self.scanTypeSelector)
        self.specSplitter.addWidget(self.scanDataSelector)
        self.specSplitter.addWidget(self.plotTypeWidget)
        self.specSplitter.addWidget(self.specDataSelector)
        self.specSplitter.addWidget(QWidget())

    def createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("File")

        openAction = QAction("Open", self)
        openAction.triggered.connect(self.openSpecFile)

        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)

        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    def createPlotTypeComboBox(self):
        """Creates the plot type QComboBox:single or multi."""
        self.plotTypeWidget = QWidget()
        self.plotTypeWidget.setFixedWidth(400)
        hLayout = QHBoxLayout()
        self.plotTypeCB = QComboBox()
        self.plotTypeCB.addItem("Single")
        self.plotTypeCB.addItem("Multi")
        self.plotTypeCB.currentIndexChanged.connect(self.updatePlot)

        hLayout.addWidget(QLabel("Plot Type: "))
        hLayout.addWidget(self.plotTypeCB)

        self.plotTypeWidget.setLayout(hLayout)

    def openSpecFile(self):
        file, specFilterName = QFileDialog.getOpenFileName(self, "Open spec file", None, "*.spec")
        self.specFile = None

        if file != "":
            try:
                self.specFileList.addSpecFile(file)
                print("File Added")
            except Exception as ex:
                QMessageBox.warning(self, "Loading error",
                                    "There was an error loading the spec file. \n\nException: " + str(ex))

    def loadScans(self, i):
        """Loads the spec information to specguiutils widgets.
        :return:
        """
        specDataFile = self.specFileList.specFileArray[i]
        indx = self.getSpecFileSelectorIndex(specDataFile)
        scanBrowser = self.scanDataSelector.scanBrowserArray[indx]
        scanBrowser.loadScans(specDataFile.getScans())
        self.updateScanTypeSelector()
        scanBrowser.scanSelected.connect(specDataFile.scanSelection)
        scanBrowser.scanSelected.connect(self.updatePlot)
        scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)

    def updateScanTypeSelector(self):
        if self.scanTypeSelector.getCurrentType() != 'All':
            self.clearScanBrowsersSelection()
        self.scanTypeSelector.loadScans(self.getAllScanTypes())
        self.filterScansByType()

    def filterScansByType(self):
        """Reloads the ScanBrowser filter by the selected scan type."""
        if self.scanTypeSelector.getCurrentType() == 'All':
            for i in self.specFileList.selectedSpecFile:
                specDataFile = self.specFileList.specFileArray[i]
                indx = self.getSpecFileSelectorIndex(specDataFile)
                scanBrowser = self.scanDataSelector.scanBrowserArray[indx]
                scanBrowser.loadScans(specDataFile.getScans())
                scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            for i in self.specFileList.selectedSpecFile:
                specDataFile = self.specFileList.specFileArray[i]
                indx = self.getSpecFileSelectorIndex(specDataFile)
                scanBrowser = self.scanDataSelector.scanBrowserArray[indx]
                scanBrowser.filterByScanTypes(specDataFile.getScans(), self.scanTypeSelector.getCurrentType())
                scanBrowser.scanList.setSelectionMode(QAbstractItemView.MultiSelection)

    def setSelectedPlotDetectors(self, detectors):
        """Method will be called when a detector is selected or unselected. """
        self.selectedDetectors = detectors
        self.updatePlot()

    def updatePlot(self):
        """This method gets called when the plot type QCombox changes index."""
        self.setSelectedScans()
        #if self.PlotWidget.specOpen is True and self.PlotWidget.scanHasBeenSelected is True:
        plotType = self.plotTypeCB.currentText()
        if plotType == "Single":
            self.PlotWidget.singlePlot(self.selectedDetectors, self.selectedScans)
        else:
            self.PlotWidget.multiPlot(self.selectedDetectors, self.selectedScans)

    def newSpecFileSelected(self, i):
        print("Row: ", i)
        specDataFile = self.specFileList.specFileArray[i]
        self.scanDataSelector.addScanBrowser(specDataFile.getSpecFileName())
        self.loadScans(i)

    def noSpecFileSelected(self, i):
        if len(self.specFileList.selectedSpecFile) == 0:
            print("No Spec file has been selected. ")
            for button in self.selectorContainer.buttonGroup.buttons():
                button.setCheckState(False)

            self.PlotWidget.clearPlot()
            self.PlotWidget.defaultPlot()
            self.scanDataSelector.defaultScanBrowser()
            self.updateScanTypeSelector()
        else:
            specDataFile = self.specFileList.specFileArray[i]
            indx = self.getSpecFileSelectorIndex(specDataFile)
            self.scanDataSelector.scanBrowserArray.pop(indx)
            self.scanDataSelector.removeTab(indx)
            self.updateScanTypeSelector()


    def getSpecFileSelectorIndex(self, specDataFile):
        """This method gets the index of the ScanBrowser and tab for the particular spec file that has been
        opened and loaded."""
        for i in range(self.scanDataSelector.count()):
            if self.scanDataSelector.tabText(i) == specDataFile.getSpecFileName():
                return i

    def getAllScanTypes(self):
        scanTypes = set()

        for i in self.specFileList.selectedSpecFile:
            specDataFile = self.specFileList.specFileArray[i]
            types = specDataFile.getScanTypes()
            print(types)
            for type in types:
                scanTypes.add(type)

        print(scanTypes)
        scanTypes = list(scanTypes)
        scanTypes.sort(key=str.lower)
        return scanTypes

    def clearScanBrowsersSelection(self):
        for i in self.specFileList.selectedSpecFile:
            specDataFile = self.specFileList.specFileArray[i]
            indx = self.getSpecFileSelectorIndex(specDataFile)
            scanBrowser = self.scanDataSelector.scanBrowserArray[indx]
            scanBrowser.scanList.clearSelection()

    def setSelectedScans(self):
        self.selectedScans = []
        for i in self.specFileList.selectedSpecFile:
            specDataFile = self.specFileList.specFileArray[i]
            scans = specDataFile.selectedScans
            for scan in scans:
                self.selectedScans.append(scan)
        print("Main Window Scans:")
        print(self.selectedScans)


def main():
    """Main method.
    """
    app = QApplication(sys.argv)
    herixWindow = HerixWorkbenchWindow()
    herixWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()