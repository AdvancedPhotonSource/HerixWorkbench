#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from matplotlib.pylab import plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import numpy as np
# ----------------------------------------End of Imports---------------------------------------------------------------#

class PlotWidget(QObject):
    """Creates the group box with the detector check boxes."""

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.mainWindow = parent
        self.plotWidget = QWidget()
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.graphNavigationBar = NavigationToolbar(self.canvas, parent)
        self.legendList = PlotLegendList()
        self.defaultPlot()
        self.detectors = []
        self.scans = []
        self.counters = []
        self.currentTab = 0
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)

        layout = QVBoxLayout()

        splitter.addWidget(self.graphNavigationBar)
        splitter.addWidget(self.canvas)
        splitter.addWidget(self.legendList)
        layout.addWidget(splitter)
        self.plotWidget.setLayout(layout)

    def defaultPlot(self):
        axes = self.fig.add_subplot(111)
        axes.plot([1, 2, 3, 4], [1, 2, 3, 4])
        self.fig.tight_layout(rect=[0 , .04, 1, 1])
        self.canvas.draw()
        self.legendList.defaultLegend()

    def singlePlot(self, detectors, scans):
        """This is the single plot that contains everything getting graphed.
        :param detectors: list of checked detectors
        :return:
        """
        self.clearPlot()
        self.detectors = detectors
        self.scans = scans

        if len(detectors) == 0:
            self.defaultPlot()
        else:
            ax = self.fig.add_subplot(111)
            ax.set_ylabel("Detector Data")
            ax.set_xlabel("Points")
            for d in detectors:
                self.singlePlotUtils(ax, d, scans)
            ax.legend(loc='upper center', fancybox=True, shadow=True, fontsize="x-small")
            self.fig.tight_layout(rect=[0, 0.1, 1, 1])
            self.canvas.draw()

    def multiPlot(self, detectors, scans):
        try:
            self.clearPlot()
            self.detectors = detectors
            self.scans = scans
            if len(scans) > 0:
                if len(detectors) == 1:
                    ax1 = self.fig.add_subplot(111)
                    self.multiPlotUtils(ax1, detectors[0], scans)
                elif len(detectors) == 2:
                   ax1 = self.fig.add_subplot(121)
                   ax2 = self.fig.add_subplot(122)

                   self.multiPlotUtils(ax1, detectors[0], scans)
                   self.multiPlotUtils(ax2, detectors[1], scans)
                elif len(detectors) == 3:
                    ax1 = self.fig.add_subplot(221)
                    ax2 = self.fig.add_subplot(222)
                    ax3 = self.fig.add_subplot(223)

                    self.multiPlotUtils(ax1, detectors[0], scans)
                    self.multiPlotUtils(ax2, detectors[1], scans)
                    self.multiPlotUtils(ax3, detectors[2], scans)
                elif len(detectors) == 4:
                    ax1 = self.fig.add_subplot(221)
                    ax2 = self.fig.add_subplot(222)
                    ax3 = self.fig.add_subplot(223)
                    ax4 = self.fig.add_subplot(224)

                    self.multiPlotUtils(ax1, detectors[0], scans)
                    self.multiPlotUtils(ax2, detectors[1], scans)
                    self.multiPlotUtils(ax3, detectors[2], scans)
                    self.multiPlotUtils(ax4, detectors[3], scans)
                elif len(detectors) == 5:
                    ax1 = self.fig.add_subplot(231)
                    ax2 = self.fig.add_subplot(232)
                    ax3 = self.fig.add_subplot(233)
                    ax4 = self.fig.add_subplot(234)
                    ax5 = self.fig.add_subplot(235)

                    self.multiPlotUtils(ax1, detectors[0], scans)
                    self.multiPlotUtils(ax2, detectors[1], scans)
                    self.multiPlotUtils(ax3, detectors[2], scans)
                    self.multiPlotUtils(ax4, detectors[3], scans)
                    self.multiPlotUtils(ax5, detectors[4], scans)
                elif len(detectors) == 6:
                    ax1 = self.fig.add_subplot(231)
                    ax2 = self.fig.add_subplot(232)
                    ax3 = self.fig.add_subplot(233)
                    ax4 = self.fig.add_subplot(234)
                    ax5 = self.fig.add_subplot(235)
                    ax6 = self.fig.add_subplot(236)

                    self.multiPlotUtils(ax1, detectors[0], scans)
                    self.multiPlotUtils(ax2, detectors[1], scans)
                    self.multiPlotUtils(ax3, detectors[2], scans)
                    self.multiPlotUtils(ax4, detectors[3], scans)
                    self.multiPlotUtils(ax5, detectors[4], scans)
                    self.multiPlotUtils(ax6, detectors[5], scans)
                elif len(detectors) == 7:
                    ax1 = self.fig.add_subplot(331)
                    ax2 = self.fig.add_subplot(332)
                    ax3 = self.fig.add_subplot(333)
                    ax4 = self.fig.add_subplot(334)
                    ax5 = self.fig.add_subplot(335)
                    ax6 = self.fig.add_subplot(336)
                    ax7 = self.fig.add_subplot(337)

                    self.multiPlotUtils(ax1, detectors[0], scans)
                    self.multiPlotUtils(ax2, detectors[1], scans)
                    self.multiPlotUtils(ax3, detectors[2], scans)
                    self.multiPlotUtils(ax4, detectors[3], scans)
                    self.multiPlotUtils(ax5, detectors[4], scans)
                    self.multiPlotUtils(ax6, detectors[5], scans)
                    self.multiPlotUtils(ax7, detectors[6], scans)
                elif len(detectors) == 8:
                    ax1 = self.fig.add_subplot(331)
                    ax2 = self.fig.add_subplot(332)
                    ax3 = self.fig.add_subplot(333)
                    ax4 = self.fig.add_subplot(334)
                    ax5 = self.fig.add_subplot(335)
                    ax6 = self.fig.add_subplot(336)
                    ax7 = self.fig.add_subplot(337)
                    ax8 = self.fig.add_subplot(338)

                    self.multiPlotUtils(ax1, detectors[0], scans)
                    self.multiPlotUtils(ax2, detectors[1], scans)
                    self.multiPlotUtils(ax3, detectors[2], scans)
                    self.multiPlotUtils(ax4, detectors[3], scans)
                    self.multiPlotUtils(ax5, detectors[4], scans)
                    self.multiPlotUtils(ax6, detectors[5], scans)
                    self.multiPlotUtils(ax7, detectors[6], scans)
                    self.multiPlotUtils(ax8, detectors[7], scans)
                elif len(detectors) >= 9:
                    ax1 = self.fig.add_subplot(331)
                    ax2 = self.fig.add_subplot(332)
                    ax3 = self.fig.add_subplot(333)
                    ax4 = self.fig.add_subplot(334)
                    ax5 = self.fig.add_subplot(335)
                    ax6 = self.fig.add_subplot(336)
                    ax7 = self.fig.add_subplot(337)
                    ax8 = self.fig.add_subplot(338)
                    ax9 = self.fig.add_subplot(339)

                    self.multiPlotUtils(ax1, detectors[0], scans)
                    self.multiPlotUtils(ax2, detectors[1], scans)
                    self.multiPlotUtils(ax3, detectors[2], scans)
                    self.multiPlotUtils(ax4, detectors[3], scans)
                    self.multiPlotUtils(ax5, detectors[4], scans)
                    self.multiPlotUtils(ax6, detectors[5], scans)
                    self.multiPlotUtils(ax7, detectors[6], scans)
                    self.multiPlotUtils(ax8, detectors[7], scans)
                    self.multiPlotUtils(ax9, detectors[8], scans)
                else:
                    self.defaultPlot()
                self.canvas.draw()
                self.fig.tight_layout()
        except Exception as e:
            QMessageBox.warning(None, "Plot error", "An error occur while plotting the selected data. \n\n"
                                              "Here's the exception: " + str(e))

    def clearPlot(self):
        """Clears the plot"""
        self.fig.clear()
        self.canvas.draw()
        self.legendList.clearLegend()

    def multiPlotUtils(self, ax, detector, scans):
        """This method uses the pass axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :param detectorData: detector data from spec file
        :return:
        """
        if len(scans) > 0:
            for scan in scans:
                detectorData = scan.getSpecDetectorData(detector)
                h, k, l, temp1, temp2, diam = scan.getPlotLegendInfo(detector)
                title = detector + " " + scan.getSpecFileName()

                xx, xLabel = scan.getDetectorXAxis()
                if scan.shiftValue is not 0:
                    xx = np.add(xx, scan.shiftValue)
                yy = detectorData
                maximum = max(yy)
                maxIndx = yy.index(maximum)
                maxPos = xx[maxIndx]
                scan.maxPos = maxPos
                scan.max = maximum

                ax.set_title(str(detector))
                plot = ax.plot(xx, yy, label=str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()))
                self.legendList.addLegend(title, temp1, temp2, h, k, l, diam, plot[0].get_color(), maximum, maxPos)
                ax.set_ylabel(str(detector))
                ax.set_xlabel(xLabel)
                ax.legend(loc='upper center', fancybox=True, shadow=True, fontsize="x-small")

    def singlePlotUtils(self, ax, detector, scans):
        """This method uses the pass axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :return:
        """
        if len(scans) > 0:
            for scan in scans:
                detectorData = scan.getSpecDetectorData(detector)
                h, k, l, temp1, temp2, diam = scan.getPlotLegendInfo(detector)
                title = detector + " " + scan.getSpecFileName()

                xx, xLabel = scan.getDetectorXAxis()
                if scan.shiftValue is not 0:
                    xx = np.add(xx, scan.shiftValue)
                yy = detectorData
                maximum = max(yy)
                maxIndx = yy.index(maximum)
                maxPos = xx[maxIndx]
                scan.maxPos = maxPos
                scan.max = maximum

                #TODO:Remove this method for one that adds a tab widget
                plot = ax.plot(xx, yy, label=str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()))
                self.legendList.addLegend(title, temp1, temp2, h, k, l, diam, plot[0].get_color(), maximum, maxPos)
                ax.set_ylabel(str(detector))
                ax.set_xlabel(xLabel)

    def shifterChanged(self, shiftInfo):
        scan, value, specFile = shiftInfo
        for s in self.scans:
            if s.getSpecFileName() == specFile and s.scan == scan:
                s.setShifter(value)

        # Calls singlePlot if plotType is "Singlge", else multiPlot
        if self.currentTab == 0:
            self.counterPlot(self.counters, self.scans)
        else:
            plotType = self.mainWindow.plotTypeCB.currentText()
            if plotType == "Single":
                self.singlePlot(self.detectors, self.scans)
            else:
                self.multiPlot(self.detectors, self.scans)

    def counterPlot(self, counters, scans):
        """
        :param counters: counters to be plot
        :param scans: scans to be plot
        :return:
        """
        print("Counters: \n", counters)
        self.counters = counters
        self.scans = scans
        self.clearPlot()

        #TODO: might not need this if here. Will counters ever have a value less than 3
        if len(counters) == 0:
            self.defaultPlot()
        else:
            xCounter, yCounter, normalizer = counters
            ax = self.fig.add_subplot(111)
            ax.set_ylabel("Detector Data")
            ax.set_xlabel("Points")
            self.counterPlotUtils(ax, scans, xCounter, yCounter, normalizer)
            ax.legend(loc='upper center', fancybox=True, shadow=True, fontsize="x-small")
            self.fig.tight_layout(rect=[0, 0.1, 1, 1])
            self.canvas.draw()

    def counterPlotUtils(self, ax, scans, xCounter, yCounter, normalizer):
        try:
            if len(scans) > 0:
                for scan in scans:
                    print("Method: counterPlotUtils")
                    print('Scan: ' + str(scan.scan))
                    print("ShifValue: ", scan.shiftValue)
                    print("SpecFile: ", scan.getSpecFileName())
                    print("End of Method: counterPlotUtils")
                    xx = scan.getSpecDetectorData(xCounter)
                    yy = scan.getSpecDetectorData(yCounter)

                    maximum = max(yy)
                    maxIndx = yy.index(maximum)
                    maxPos = xx[maxIndx]
                    scan.maxPos = maxPos
                    scan.max = maximum

                    if normalizer.find("PyQt") == -1:
                        mon = scan.getSpecDetectorData(normalizer)
                        yy = np.divide(yy, mon)

                    if scan.shiftValue is not 0:
                        xx = np.add(xx, scan.shiftValue)

                    label = (str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()))
                    plot = ax.plot(xx, yy, label=str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()))
                    self.legendList.addLegend(label, 0, 0, 0, 0, 0, 0, plot[0].get_color(), maximum, maxPos)
                    ax.set_ylabel(yCounter)
                    ax.set_xlabel(xCounter)
        except Exception as ex:
            QMessageBox.warning(None, "Error", "Please make sure the scan " + scan.scan + " from the spec file " +
                                scan.getSpecFileName() + " contains the counters trying to be plotted. "
                                               " \n\nError: " + str(ex))

class PlotLegendList(QTabWidget):
    """It uses a QListWidget to display the legend information."""

    def __init__(self):
        super(PlotLegendList, self).__init__()
        self.setMaximumHeight(300)
        self.setFixedHeight(100)
        #self.setFont(QFont("Helvetica", 12, QFont.Bold))
        self.defaultLegend()

    def addLegend(self, title, temp1, temp2, h, k, l, diam, color, maximum, maxPos):
        legend = PlotLegend()
        legend.setValuesOnLegend(temp1, temp2, h, k, l, diam, maximum, maxPos)
        self.addTab(legend, title)

    def defaultLegend(self):
        self.clearLegend()
        legend = PlotLegend()
        self.addTab(legend, "Default")

    def clearLegend(self):
        if self.count() > 0:
            for i in range(self.count()):
                self.removeTab(0)

class PlotLegend(QWidget):

    def __init__(self, parent=None):
        super(PlotLegend, self).__init__(parent)
        self.initializeComponentes()

    def initializeComponentes(self):
        self.vLayout = QVBoxLayout()
        self.hLayout1 = QHBoxLayout()
        self.hLayout2 = QHBoxLayout()

        self.tempLbl = QLabel("Temp:")
        self.temp1 = QLineEdit()
        self.temp1.setReadOnly(True)
        self.temp2 = QLineEdit()
        self.temp2.setReadOnly(True)
        self.hLbl = QLabel("H:")
        self.H = QLineEdit()
        self.H.setReadOnly(True)
        self.kLbl = QLabel("K:")
        self.K = QLineEdit()
        self.K.setReadOnly(True)
        self.lLbl = QLabel("L:")
        self.L = QLineEdit()
        self.L.setReadOnly(True)
        self.diamLbl = QLabel("Diam:")
        self.diam = QLineEdit()
        self.diam.setReadOnly(True)
        self.peakLbl = QLabel("Peak:")
        self.peakMax = QLineEdit()
        self.peakMax.setReadOnly(True)
        self.positionLbl = QLabel("Position:")
        self.position = QLineEdit()
        self.position.setReadOnly(True)
        self.widthLbl = QLabel("Width:")
        self.width = QLineEdit()
        self.width.setReadOnly(True)


        self.hLayout1.addWidget(self.tempLbl)
        self.hLayout1.addWidget(self.temp1)
        self.hLayout1.addWidget(self.temp2)
        self.hLayout1.addWidget(self.hLbl)
        self.hLayout1.addWidget(self.H)
        self.hLayout1.addWidget(self.kLbl)
        self.hLayout1.addWidget(self.K)
        self.hLayout1.addWidget(self.lLbl)
        self.hLayout1.addWidget(self.L)

        self.hLayout2.addWidget(self.diamLbl)
        self.hLayout2.addWidget(self.diam)
        self.hLayout2.addWidget(self.peakLbl)
        self.hLayout2.addWidget(self.peakMax)
        self.hLayout2.addWidget(self.positionLbl)
        self.hLayout2.addWidget(self.position)
        self.hLayout2.addWidget(self.widthLbl)
        self.hLayout2.addWidget(self.width)

        self.vLayout.addLayout(self.hLayout1)
        self.vLayout.addLayout(self.hLayout2)
        self.setLayout(self.vLayout)

    def initializeCounterComponents(self):
        pass

    def setValuesOnLegend(self, temp1, temp2, h, k, l, diam, maximum, maxPos):
        self.temp1.setText(str(temp1))
        self.temp2.setText(str(temp2))
        self.H.setText(str(h))
        self.K.setText(str(k))
        self.L.setText(str(l))
        self.diam.setText(str(diam))
        self.peakMax.setText(str(maximum))
        self.position.setText(str(maxPos))


