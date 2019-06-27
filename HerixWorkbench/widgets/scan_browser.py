#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import PyQt5.QtGui as qtGui
from PyQt5.Qt import QValidator
import logging
import gc
from specguiutils import METHOD_ENTER_STR
from HerixWorkbench.tools.scan import Scan
# ---------------------------------------------------------------------------------------------------------------------#

logger = logging.getLogger(__name__)

SCAN_COL_WIDTH = 40
CMD_COL_WIDTH = 240
NUM_PTS_COL_WIDTH = 65
SHIFT_COL_WIDTH = 85
MINIMUM_WIDGET_WIDTH = 420
SCAN_COL = 0
CMD_COL = 1
NUM_PTS_COL = 2
SHIFT_COL = 3
DEFAULT_COLUMN_NAMES = ['S#', 'Command', 'Points', 'Shift']


class ScanBrowser(qtWidgets.QWidget):
    """
    This class provides information about scans in a spec file.  By default,
    scan number, the scan command and number of points each in a column in the
    table.  This class can be combined with other classes such as the
    :py:class:.ScanTypeSelector and :py:class:.PositionerSelector to provide
    more function.
    :py:class:.ScanTypeSelector allows the user to select a
    particular scan type or All scan Types.
    :py:class:.PositionerSelector allows the user to select from a list of
    positioners available in the scan. The results of this selection can be fed
    back in via :py:func:setPositionersToDisplay.  This will add an additional
    column to the table for each positioner listed in the scan.  The list of
    positioners is given in the #P fields in the file header and the values
    to display are from the corresponding #O values in the scan header.

    This class was made by John Hammonds, it's from his package specguiutils.
    I made some changes to better fit my program.
    """
    # Define some signals that this class will provide to users
    scanSelected = qtCore.pyqtSignal(dict, name="scanSelected")
    scanLoaded = qtCore.pyqtSignal(bool, name="scanLoaded")
    shifterChanged = qtCore.pyqtSignal(list, name="shifterChanged")

    def __init__(self, parent=None):
        """
        Construct an empty table with columns for scan number, scan command and
        number of points.  Data is added to the table via the :py:func:loadScans
        command
        """
        super(ScanBrowser, self).__init__(parent)
        layout = qtWidgets.QHBoxLayout()
        self.specFile = None
        self.positionersToDisplay = []
        self.userParamsToDisplay = []
        self.lastScans = None
        self.scanList = qtWidgets.QTableWidget()
        self.prevSelectedScans = {}
        self.scans = {}
        self.scanType = "All"
        self.primaryScan = None  # Last selected scan

        font = qtGui.QFont("Helvetica", pointSize=10)
        self.scanList.setFont(font)
        self.scanList.setEditTriggers(qtWidgets.QAbstractItemView.NoEditTriggers)
        self.scanList.setColumnCount(len(DEFAULT_COLUMN_NAMES) + len(self.positionersToDisplay))
        self.scanList.setColumnWidth(SCAN_COL, SCAN_COL_WIDTH)
        self.scanList.setColumnWidth(CMD_COL, CMD_COL_WIDTH)
        self.scanList.setColumnWidth(NUM_PTS_COL, NUM_PTS_COL_WIDTH)
        self.scanList.setColumnWidth(SHIFT_COL, SHIFT_COL_WIDTH)
        self.scanList.setHorizontalHeaderLabels(['S#', 'Command', 'Points', 'Shift'])
        self.scanList.verticalHeader().setVisible(False)
        self.scanList.setSelectionBehavior(qtWidgets.QAbstractItemView.SelectRows)
        self.scanList.setFocusPolicy(qtCore.Qt.NoFocus)
        self.setMinimumWidth(400)
        self.setMaximumWidth(900)
        self.setMinimumHeight(250)
        layout.addWidget(self.scanList)
        self.setLayout(layout)

        self.scanList.itemSelectionChanged.connect(self.scanSelectionChanged)

    def loadScans(self, scans, specFile):
        """Creates a Scan() and fills the scans dictionary.
        """
        for scan in scans:
            self.scans.update({scan: Scan(scan, specFile)})

    def loadScanBrowser(self, scans, newFile=True):
        """
        loads the list of scans into the browser. At the end, it will
        pass emit a message that the scan is loaded and from the input
        newFile, it will pass along whether or not this is a new file.
        This is helpful when the scan is reloaded with just a single
        type of scan.  This causes recognition that this is not an
        overall change of file, just changing to a subset of the list.
        """
        logger.debug(METHOD_ENTER_STR)
        self.lastScans = scans
        self.scanList.itemSelectionChanged.disconnect(self.scanSelectionChanged)
        self.scanList.setRowCount(len(scans.keys()))
        scanKeys = sorted(scans, key=int)
        logger.debug("scanKeys %s" % str(scanKeys))
        row = 0
        for key in scanKeys:
            scan = self.scans[key]
            scan.tableRow = row

            scanItem = qtWidgets.QTableWidgetItem(str(scans[key].scanNum))
            self.scanList.setItem(row, SCAN_COL, scanItem)

            cmdItem = qtWidgets.QTableWidgetItem(scans[key].scanCmd)
            self.scanList.setItem(row, CMD_COL, cmdItem)

            nPointsItem = qtWidgets.QTableWidgetItem(str(len(scans[key].data_lines)))
            self.scanList.setItem(row, NUM_PTS_COL, nPointsItem)

            shiftItem = LineShifter()
            shiftItem.valueChanged.connect(self.shifterValueChanged)
            scan.plotShifter = shiftItem
            self.scanList.setCellWidget(row, SHIFT_COL, shiftItem)
            row += 1

        self.fillSelectedPositionerData()
        self.fillSelectedUserParamsData()
        self.scanList.itemSelectionChanged.connect(self.scanSelectionChanged)
        self.scanLoaded.emit(newFile)

    def fillSelectedPositionerData(self):
        """
        If positioners have been selected to supplement the table, then
        this cause will grab the values out for each scan and places it
        in a column of the table
        """
        if self.lastScans is None:
            return
        scanKeys = sorted(self.lastScans, key=int)
        row = 0
        if (not (self.lastScans is None)) and (len(self.positionersToDisplay)) > 0:
            for scan in scanKeys:
                posNum = 1
                for positioner in self.positionersToDisplay:
                    item = qtWidgets.QTableWidgetItem(str(self.lastScans[scan].positioner[positioner]))
                    self.scanList.setItem(row, NUM_PTS_COL + posNum, item)
                    posNum += 1
                row += 1

    def fillSelectedUserParamsData(self):
        """
        If user parameters have been selected to supplement the table,
        then this cause will grab the values out for each scan and
        places it in a column of the table
        """
        if self.lastScans is None:
            return
        scanKeys = sorted(self.lastScans, key=int)
        row = 0
        if (not (self.lastScans is None)) and (len(self.userParamsToDisplay)) > 0:
            for scan in scanKeys:
                posNum = 1
                for userParam in self.userParamsToDisplay:
                    try:
                        item = qtWidgets.QTableWidgetItem(str(self.lastScans[scan].U[userParam]))
                        self.scanList.setItem(row, \
                                              NUM_PTS_COL + posNum \
                                              + len(self.positionersToDisplay), \
                                              item)
                    except KeyError:
                        item = qtWidgets.QTableWidgetItem(str("N/A"))
                        self.scanList.setItem(row, \
                                              NUM_PTS_COL + posNum \
                                              + len(self.positionersToDisplay), \
                                              item)
                    posNum += 1
                row += 1

    def filterByScanTypes(self, scans, scanTypes):
        """
        selects scans fron the list that have a given scan Type and
        causes these to be loaded into the scan table.
        """
        print("Filter by scan")
        filteredScans = {}
        scanKeys = sorted(scans, key=int)
        if scanTypes is None:
            raise ValueError("Invalid ScanFilter %s" % scanTypes)
        for scan in scanKeys:
            if len(scanTypes) > 0:
                if self.isNumber(scans[scan].scanCmd.split()[1]):
                    thisType = scans[scan].scanCmd.split()[0]
                else:
                    thisType = scans[scan].scanCmd.split()[0] + " " + scans[scan].scanCmd.split()[1]

                if thisType in scanTypes:
                    filteredScans[scan] = scans[scan]
            else:
                filteredScans[scan] = scans[scan]
        logger.debug ("Filtered Scans %s" % filteredScans)

        self.clear()
        return filteredScans

    def clear(self):
        self.scanList.itemSelectionChanged.disconnect(self.scanSelectionChanged)
        self.scanList.clearSelection()
        self.scanList.itemSelectionChanged.connect(self.scanSelectionChanged)

    def isNumber(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def getCurrentScan(self):
        """
        retifmx the currently selected scan
        """
        return str(self.scanList.item(self.scanList.currentRow(), 0).text())

    def setCurrentScan(self, row):
        """
        Sets the current scan selection
        """
        self.scanList.setCurrentCell(row, 0)

    def setPositionersToDisplay(self, positioners):
        """
        Sets a list of positiorers that will be added to the table
        whenever new data is loaded
        """
        self.positionersToDisplay = positioners
        self.scanList.setColumnCount(len(DEFAULT_COLUMN_NAMES) + \
                                     len(self.positionersToDisplay) + \
                                     len(self.userParamsToDisplay))
        self.scanList.setHorizontalHeaderLabels(DEFAULT_COLUMN_NAMES + \
                                            self.positionersToDisplay + \
                                            self.userParamsToDisplay)
        self.fillSelectedPositionerData()
        self.fillSelectedUserParamsData()

    def setUserParamsToDisplay(self, userParams):
        """Sets a list of positiorers that will be added to the table
        whenever new data is loaded
        """
        self.userParamsToDisplay = userParams
        self.scanList.setColumnCount(len(DEFAULT_COLUMN_NAMES) + \
                                     len(self.positionersToDisplay) + \
                                     len(self.userParamsToDisplay))
        self.scanList.setHorizontalHeaderLabels(DEFAULT_COLUMN_NAMES + \
                                            self.positionersToDisplay +
                                            self.userParamsToDisplay)
        self.fillSelectedPositionerData()
        self.fillSelectedUserParamsData()

    def scanSelectionChanged(self):
        """This method runs when a scan ix selected.
        """
        print("scan_selection_scanBrowser")
        logger.debug(METHOD_ENTER_STR)
        selectedItems = self.scanList.selectedIndexes()

        #  Ensures that there must be a scan selected
        if len(selectedItems) == 0:
            self.scanList.itemSelectionChanged.disconnect(self.scanSelectionChanged)
            self.setCurrentScan(self.prevSelectedScans[next(iter(self.prevSelectedScans))].tableRow)
            self.scanList.itemSelectionChanged.connect(self.scanSelectionChanged)
            return

        logger.debug("SelectedItems %s" % selectedItems)
        selectedScans = {}
        for item in selectedItems:
            if item.column() == 0:
                scanNum = str(self.scanList.item(item.row(), 0).text())
                scan = self.scans[scanNum]
                scan.createDetectorInfoDictionary()
                shifter = self.scanList.cellWidget(item.row(), 3)
                shifter.setEnabled(True)
                selectedScans.update({scanNum: scan})

                # Deletes the scan from previously selected scans, if it's still selected
                if scanNum in self.prevSelectedScans:
                    self.prevSelectedScans.pop(scanNum, None)

        # Sets the shifter of the unselected scans enable to false
        for s in self.prevSelectedScans:
            scan = self.scans[s]
            shifter = self.scanList.cellWidget(scan.tableRow, 3)
            shifter.setValue(0)
            shifter.setEnabled(False)
            shifter.clearFocus()
        self.prevSelectedScans.clear()

        logger.debug("Selected scans %s" % selectedScans)
        self.prevSelectedScans = selectedScans

        self.scanSelected[dict].emit(selectedScans)


    def shifterValueChanged(self, val):
        """This method emits a signal, passing a list, shiftInfo --> (has scanNum, shiftVal, specFile)
        """
        self.scanSelected[dict].emit(self.prevSelectedScans)


class LineShifter(qtWidgets.QDoubleSpinBox):
    """This class creates a QSpinBox widget that will raise an event to shift the function graphed in PlotWidget.
    """
    shifterChanged = qtCore.pyqtSignal(list, name="shifterChanged")

    def __init__(self):
        super(LineShifter, self).__init__(parent=None)
        self.setDecimals(3)
        self.setSingleStep(.1)
        self.row = ""
        self.setMaximum(100)
        self.setMinimum(-100)
        self.setEnabled(False)
        self.setAttribute(qtCore.Qt.WA_MacShowFocusRect, False)

    def value(self):
        try:
            return float(self.text())
        except:
            return 0
