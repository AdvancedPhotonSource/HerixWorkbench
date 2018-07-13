#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from HerixWorkbench.tools.specDataSelector import SpecDataSelector
from specguiutils.scantypeselector import ScanTypeSelector
from HerixWorkbench.source.DetectorSelector import SelectorContainer
from HerixWorkbench.source.PlotWidget import PlotWidget
from HerixWorkbench.source.SpecFileSelector import SpecFileSelectionList
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
        self.specDataSelector = SpecDataSelector()
        self.scanTypeSelector = ScanTypeSelector()
        self.selectorContainer = SelectorContainer()
        self.selectorContainer.detectorsSelected.connect(self.setSelectedPlotDetectors)

        self.specSplitter.addWidget(self.specFileList)
        self.specSplitter.addWidget(self.scanTypeSelector)
        self.specSplitter.addWidget(self.specDataSelector)
        self.specSplitter.addWidget(self.plotTypeWidget)
        self.specSplitter.addWidget(self.selectorContainer)
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
                if self.specFileList.specFileList.count() == 1:
                    i = 0
                    specDataFile = self.specFileList.specFileArray[i]
                    self.specDataSelector.addScanBrowser(specDataFile.getSpecFileName())
                    self.loadScans(i)
            except Exception as ex:
                QMessageBox.warning(self, "Loading error",
                                    "There was an error loading the spec file. \n\nException: " + str(ex))

    def loadScans(self, i):
        """Loads the spec information to specguiutils widgets.
        :return:
        """
        specDataFile = self.specFileList.specFileArray[i]
        scanBrowser = self.specDataSelector.scanBrowserArray[i]
        scanBrowser.loadScans(specDataFile.getScans())
        self.scanTypeSelector.loadScans(specDataFile.getScanTypes())
        self.scanTypeSelector.scanTypeChanged.connect(self.filterScansByType)
        scanBrowser.scanSelected.connect(self.PlotWidget.scanSelection)
        scanBrowser.scanSelected.connect(self.updatePlot)
        scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)


    def filterScansByType(self):
        """Reloads the ScanBrowser filter by the selected scan type."""
        if self.scanTypeSelector.getCurrentType() == 'All':
            self.scanBrowser.loadScans(self.scans)
            self.scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            self.scanBrowser.filterByScanTypes(self.scans, self.scanTypeSelector.getCurrentType())
            self.scanBrowser.scanList.setSelectionMode(QAbstractItemView.MultiSelection)

    def setSelectedPlotDetectors(self, detectors):
        """Method will be called when a detector is selected or unselected. """
        self.selectedDetectors = detectors
        self.updatePlot()

    def updatePlot(self):
        """This method gets called when the plot type QCombox changes index."""
        if self.PlotWidget.specOpen is True and self.PlotWidget.scanHasBeenSelected is True:
            plotType = self.plotTypeCB.currentText()
            if plotType == "Single":
                self.PlotWidget.singlePlot(self.selectedDetectors)
            else:
                self.PlotWidget.multiPlot(self.selectedDetectors)

    def newSpecFileSelected(self, specFiles):
        print(specFiles)
        print("hi")
        #self.PlotWidget.loadSpecFile(self.specFileList.specFileArray[int])
        #self.scans = self.PlotWidget.getScans()
        #self.loadScans()

    def noSpecFileSelected(self):

        if len(self.specFileList.selectedSpecFile) == 0:
            print("No Spec file has been selected. ")
            for button in self.selectorContainer.buttonGroup.buttons():
                button.setCheckState(False)

            self.PlotWidget.clearPlot()
            self.PlotWidget.defaultPlot()
            self.specDataSelector.defaultScanBrowser()

def main():
    """Main method.
    """
    app = QApplication(sys.argv)
    herixWindow = HerixWorkbenchWindow()
    herixWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()