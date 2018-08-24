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
# ----------------------------------------End of Imports---------------------------------------------------------------#

class PlotWidget(QObject):
    """Creates the group box with the detector check boxes."""

    def __init__(self):
        super(PlotWidget, self).__init__()
        self.plotWidget = QWidget()
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.defaultPlot()
        self.legendList = PlotLegendList()
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)

        layout = QVBoxLayout()
        splitter.addWidget(self.canvas)
        splitter.addWidget(self.legendList)
        layout.addWidget(splitter)
        self.plotWidget.setLayout(layout)

    def defaultPlot(self):
        axes = self.fig.add_subplot(111)
        axes.plot([1, 2, 3, 4], [1, 2, 3, 4])
        self.fig.tight_layout(rect=[0 , .04, 1, 1])
        self.canvas.draw()

    def singlePlot(self, detectors, scans):
        """This is the single plot that contains everything getting graphed.
        :param detectors: list of checked detectors
        :return:
        """
        self.clearPlot()
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
        if (len(scans) > 0):
            for scan in scans:
                detectorData = scan.getSpecDetectorData(detector)
                h, k, l, diam = scan.getPlotLegendInfo(detector)
                label = (str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()) + ": " + str(detector) + " -" +
                         " H: " + str(h) + ", K: " + str(k) + ", L: " + str(l) + ", Diam: " + str(diam))
                xx, xLabel = scan.getDetectorXAxis()
                yy = detectorData
                ax.set_title(str(detector))
                self.legendList.addLabel(str(label))
                plotSample = ax.plot(xx, yy, label=str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()))
                print(plotSample[0].get_color())
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
                h, k, l, diam = scan.getPlotLegendInfo(detector)
                label = (str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()) + ": " + str(detector) + " -" +
                         " H: " + str(h) + ", K: " + str(k) + ", L: " + str(l) + ", Diam: " + str(diam))
                xx, xLabel = scan.getDetectorXAxis()
                yy = detectorData
                self.legendList.addLabel(str(label))
                ax.plot(xx, yy, label=str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()))
                ax.set_ylabel(str(detector))
                ax.set_xlabel(xLabel)

    def counterPlot(self, counters, scans):
        self.clearPlot()
        if len(counters) == 0:
            self.defaultPlot()
        else:
            xCounter, yCounter, normalizer = counters
            print(normalizer.find("PyQt"))
            if normalizer.find("PyQt") != -1:
                print("Object")


class PlotLegendList(QListWidget):
    """It uses a QListWidget to display the legend information."""

    def __init__(self):
        super(PlotLegendList, self).__init__()
        self.setMaximumHeight(300)
        self.setFixedHeight(100)
        self.setFont(QFont("Helvetica", 12, QFont.Bold))

    def addLabel(self, label):
        self.addItem(label)

    def clearLegend(self):
        self.clear()




