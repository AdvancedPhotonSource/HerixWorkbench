#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""

# ---------------------------------------- Imports --------------------------------------------------------------------#
from __future__ import unicode_literals

import sys

import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
from HerixWorkbench.widgets.spec_file_list import SpecFileList
from HerixWorkbench.widgets.scan_browser_picker import ScanBrowserPicker
from HerixWorkbench.widgets.plot import Plot
from HerixWorkbench.widgets.spec_data_selector import SpecDataSelector
from specguiutils.scantypeselector import ScanTypeSelector
import traceback
# ---------------------------------------------------------------------------------------------------------------------#


class HerixWorkbenchWindow(qtWidgets.QMainWindow):

    """Main window that initialaizes components"""
    def __init__(self, parent=None):
        super(HerixWorkbenchWindow, self).__init__(parent)
        self.setGeometry(50, 50, 1500, 800)
        self.setWindowTitle("Herix Workbench")
        self.setMinimumSize(1000, 650)

        self.plot = Plot(self)
        self.selectedANADetectors = []
        self.selectedCounters = []
        self.selectedScans = []
        self.primarySpecFile = None
        self.primaryCounter = None
        self.specDataTab = 0

        self.windowSplitter = qtWidgets.QSplitter()
        self.CreateSpecDataSplitter()
        self.createMenuBar()
        self.windowSplitter.addWidget(self.specSplitter)
        self.windowSplitter.addWidget(self.plot)
        self.setCentralWidget(self.windowSplitter)

    def CreateSpecDataSplitter(self):
        """Creates the QSplitter with the spec and detector widgets."""
        self.specSplitter = qtWidgets.QSplitter()
        self.specSplitter.setFixedWidth(480)
        self.specSplitter.setOrientation(qtCore.Qt.Vertical)

        self.createPlotTypeComboBox()

        self.specFileList = SpecFileList()
        self.specFileList.specFileSelected.connect(self.spec_file_selected)
        self.specFileList.specFileRemoved.connect(self.spec_file_removed)
        self.specFileList.loadCounters.connect(self.load_counters)
        self.specFileList.update_plot.connect(self.updatePlot)

        self.scanBrowserPicker = ScanBrowserPicker()

        self.scanTypeSelector = ScanTypeSelector()
        self.scanTypeSelector.scanTypeChanged.connect(self.filterScansByType)

        self.specDataSelector = SpecDataSelector()
        self.specDataSelector.tabChanged.connect(self.specDataTabChanged)
        self.specDataSelector.detectorsSelected.connect(self.setSelectedPlotDetectors)
        self.specDataSelector.countersSelected.connect(self.setSelectedCounters)

        fit_btn = qtWidgets.QPushButton("Fit")
        fit_btn.pressed.connect(self.plot.show_fit_dialog)
        fitBtnLyt = qtWidgets.QHBoxLayout()
        fitBtnLyt.addStretch()
        fitBtnLyt.addWidget(fit_btn)
        fitBtnWidget = qtWidgets.QWidget()
        fitBtnWidget.setLayout(fitBtnLyt)

        self.specSplitter.addWidget(self.specFileList)
        self.specSplitter.addWidget(self.scanTypeSelector)
        self.specSplitter.addWidget(self.scanBrowserPicker)
        self.specSplitter.addWidget(self.plotTypeWidget)
        self.specSplitter.addWidget(self.specDataSelector)
        self.specSplitter.addWidget(fitBtnWidget)
        self.specSplitter.addWidget(qtWidgets.QWidget())

    def createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        fileMenu = menuBar.addMenu("File")

        openAction = qtWidgets.QAction("Open", self)
        openAction.triggered.connect(self.openSpecFile)

        exitAction = qtWidgets.QAction("Exit", self)
        exitAction.triggered.connect(self.close)

        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

    def createPlotTypeComboBox(self):
        """Creates the plotTypeWidget QComboBox:single or multi
        """

        self.plotTypeWidget = qtWidgets.QWidget()
        self.plotTypeWidget.setFixedWidth(400)
        hLayout = qtWidgets.QHBoxLayout()

        self.plotTypeCB = qtWidgets.QComboBox()
        self.plotTypeCB.addItem("Single")
        self.plotTypeCB.addItem("Multi")
        self.plotTypeCB.currentIndexChanged.connect(self.updatePlot)

        hLayout.addWidget(qtWidgets.QLabel("Plot Type: "))
        hLayout.addWidget(self.plotTypeCB)

        self.plotTypeWidget.setLayout(hLayout)

    def openSpecFile(self):
        """ Loads a spec file and adds it to the SpecFileList
        :return:
        """
        file, specFilterName = qtWidgets.QFileDialog.getOpenFileName(self, "Open spec file", "", "*.spec")
        #self.specFile = None

        if file != "":
            try:
                self.specFileList.addSpecFile(file)
            except Exception as ex:
                qtWidgets.QMessageBox.warning(self, "Loading error",
                                                    "There was an error loading the spec file. "
                                                    "\n\nException: " + str(ex))

    def spec_file_selected(self, specFile):
        """Response to signal emitted from SpecFileList when
        a new spec file gets selected
        :param specFile: returns the selected specFile
        """
        specFile.loadScanBrowser()
        self.scanBrowserPicker.addScanBrowser(specFile)
        specFile.scanBrowser.setCurrentScan(0)

        if self.scanTypeSelector.getCurrentType() != 'All':
            self.filterScansByType()

        if len(self.specFileList.specFileList) == 1:
            self.primarySpecFile = specFile
            self.scanTypeSelector.loadScans(self.primarySpecFile.getScanTypes())

    def spec_file_removed(self, specFile):
        #  TODO: I need to clear the selection of scan in the
        #   specFile and clear the selection list
        print("Spec File Removed: " + specFile.getSpecFileName())
        self.scanBrowserPicker.removeSpecFileScanBrowser(specFile)
        specFile.scanBrowser.scanSelected.disconnect(specFile.scanSelection)
        self.specFileList.selectedScans = []
        self.primaryCounter = None

        if self.primarySpecFile == specFile and len(self.specFileList.selectedSpecFiles) > 0:
            self.primarySpecFile = self.specFileList.selectedSpecFiles[0]
            self.scanTypeSelector.loadScans(self.primarySpecFile.getScanTypes())

        self.filterScansByType()


    def load_scan_types(self, specFile):
        """Loads the scan types of the first selected spec file"""
        self.scanTypeSelector.loadScans(specFile.getScanTypes())

    def load_counters(self, specFile):
        """Loads the spec labels on the counterSelector"""
        if self.primaryCounter != self.specFileList.selectedSpecFiles[0].getSpecLabels()[0]:
            print("I'm reloading counters")
            self.specFileList.selectedScans = []
            self.primaryCounter = self.specFileList.selectedSpecFiles[0].getSpecLabels()[0]
            self.specDataSelector.loadCounters(specFile.getSpecLabels())

    def filterScansByType(self):
        """Reloads the ScanBrowser filter by the selected scan type."""
        for specFile in self.specFileList.selectedSpecFiles:
            scanBrowser = specFile.scanBrowser
            if self.scanTypeSelector.getCurrentType() == 'All':
                specFile.loadScanBrowser()
                scanBrowser.scanList.setSelectionMode(qtWidgets.QAbstractItemView.SingleSelection)
                specFile.clearScanBrowserSelection()
                scanBrowser.scanList.setCurrentCell(scanBrowser.primaryScan.tableRow, 2)
            else:
                filteredScans = scanBrowser.filterByScanTypes(specFile.getScans(), self.scanTypeSelector.getCurrentType())
                scanBrowser.loadScanBrowser(filteredScans)
                scanBrowser.scanList.setSelectionMode(qtWidgets.QAbstractItemView.MultiSelection)
                specFile.clearScanBrowserSelection()

                if scanBrowser.primaryScan.scan in filteredScans and len(filteredScans) != 0:
                    scanBrowser.scanList.setCurrentCell(scanBrowser.primaryScan.tableRow, 2)
                else:
                    scanBrowser.scanList.setCurrentCell(0, 2)

        self.updatePlot()

    def specDataTabChanged(self, index):
        """Method gets activated when the tab changes
        on the specDataSelector
        """
        self.specDataTab = index
        self.plot.currentTab = index
        self.updatePlot()

    def setSelectedPlotDetectors(self, detectors):
        """Method will be called when a detector is selected or unselected.
        """
        self.selectedANADetectors = detectors
        self.updatePlot()

    def setSelectedCounters(self, selectedCounters):
        """Method gets call when a new counter is selected.
        """
        self.selectedCounters = selectedCounters
        self.updatePlot()

    def updatePlot(self):
        """
        This method gets called when the plot type QCombox changes index.
        """
        if len(self.specFileList.selectedScans) > 0:
            if self.specDataTab == 0 and len(self.selectedCounters) > 0:
                self.plot.counterPlot(self.selectedCounters, self.specFileList.selectedScans)
            elif self.specDataTab == 1 and len(self.selectedANADetectors) > 0:
                plotType = self.plotTypeCB.currentText()
                if plotType == "Single":
                    self.plot.singlePlot(self.selectedANADetectors, self.specFileList.selectedScans)
                else:
                    self.plot.multiPlot(self.selectedANADetectors, self.specFileList.selectedScans)
            else:
                self.plot.defaultPlot()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def main():
    """Main method
    """
    app = qtWidgets.QApplication(sys.argv)
    herixWorkbenchWindow = HerixWorkbenchWindow()
    herixWorkbenchWindow.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


if __name__ == '__main__':
     main()
