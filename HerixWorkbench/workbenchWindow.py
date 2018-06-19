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
from HerixWorkbench.tools.scanbrowser import ScanBrowser
from specguiutils.scantypeselector import ScanTypeSelector
from HerixWorkbench.source.DetectorSelector import SelectorContainer
from HerixWorkbench.source.PlotWidget import PlotWidget
from HerixWorkbench.source.SpecFileSelector import SpecFileSelectionList




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
        self.specFileList.noSpecFileSelected.connect(self.noSpecFileSelection)
        self.scanBrowser = ScanBrowser()
        self.scanTypeSelector = ScanTypeSelector()
        self.selectorContainer = SelectorContainer()
        self.selectorContainer.detectorsSelected.connect(self.setSelectedPlotDetectors)

        self.specSplitter.addWidget(self.specFileList)
        self.specSplitter.addWidget(self.scanTypeSelector)
        self.specSplitter.addWidget(self.scanBrowser)
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
                self.specFileList.addSpecFile(file, self.PlotWidget.specShortName(file))
                if self.specFileList.specFileList.count() == 1:
                    self.PlotWidget.loadSpecFile(file)
                    self.scans = self.PlotWidget.getScans()
                    self.loadScans()
            except Exception as ex:
                QMessageBox.warning(self, "Loading error",
                                    "There was an error loading the spec file. \n\nException: " + str(ex))

    def loadScans(self):
        """Loads the spec information to specguiutils widgets.
        :return:
        """
        self.scanBrowser.loadScans(self.scans)
        scanTypes = self.PlotWidget.getScanTypes()
        self.scanTypeSelector.loadScans(scanTypes)
        self.scanTypeSelector.scanTypeChanged.connect(self.filterScansByType)
        self.scanBrowser.scanSelected.connect(self.PlotWidget.scanSelection)
        self.scanBrowser.scanSelected.connect(self.updatePlot)
        self.scanBrowser.scanList.setSelectionMode(QAbstractItemView.SingleSelection)


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

    def newSpecFileSelected(self, int):
        self.noSpecFileSelection()
        self.PlotWidget.loadSpecFile(self.specFileList.specFileArray[int])
        self.scans = self.PlotWidget.getScans()
        self.loadScans()

    def noSpecFileSelection(self):
        print("You've entered no spec file has been selected")
        self.scanBrowser.scanList.itemSelectionChanged.disconnect(self.scanBrowser.scanSelectionChanged)
        self.selectorContainer.detectorsSelected.disconnect(self.setSelectedPlotDetectors)

        self.PlotWidget.scanHasBeenSelected = False
        self.selectedDetectors = []
        self.PlotWidget.selectedScans = []
        self.scanBrowser.scanList.clearSelection()

        for i in range(0, self.scanBrowser.scanList.rowCount()):
            print(i)
            self.scanBrowser.scanList.removeRow(0)

        for button in self.selectorContainer.buttonGroup.buttons():
            button.setCheckState(False)

        self.selectorContainer.detectorsSelected.connect(self.setSelectedPlotDetectors)
        self.scanBrowser.scanList.itemSelectionChanged.connect(self.scanBrowser.scanSelectionChanged)
        self.PlotWidget.clearPlot()

def main():
    """Main method.
    """
    app = QApplication(sys.argv)
    herixWindow = HerixWorkbenchWindow()
    herixWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()