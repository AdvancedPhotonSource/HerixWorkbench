#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.pylab import plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from HerixWorkbench.source.SpecData import SpecData
# ----------------------------------------End of Imports---------------------------------------------------------------#

class PlotWidget(SpecData):
    """Creates the group box with the detector check boxes."""

    def __init__(self):
        super(PlotWidget, self).__init__()
        self.plotWidget = QWidget()
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.defaultPlot()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.plotWidget.setLayout(layout)

    def defaultPlot(self):
        axes = self.fig.add_subplot(111)
        axes.plot([1, 2, 3, 4], [1, 2, 3, 4])
        self.canvas.draw()

    def singlePlot(self, detectors):
        """This is the single plot that contains everything getting graphed.
        :param detectors: list of checked detectors
        :return:
        """
        self.clearPlot()
        if len(detectors) == 0:
            self.defaultPlot()
        else:
            ax = self.fig.add_subplot(111)
            ax.set_title(str(self.specShortName(self.specFilePath)))
            ax.set_ylabel("Detector Data")
            ax.set_xlabel("Points")
            for d in detectors:
                self.singlePlotUtils(ax, d)
            ax.legend()

            self.canvas.draw()

    def multiPlot(self, detectors):
        try:
            self.clearPlot()

            if len(detectors) == 1:
                ax1 = self.fig.add_subplot(111)
                self.multiPlotUtils(ax1, detectors[0])
            elif len(detectors) == 2:
               ax1 = self.fig.add_subplot(121)
               ax2 = self.fig.add_subplot(122)

               self.multiPlotUtils(ax1, detectors[0])
               self.multiPlotUtils(ax2, detectors[1])
            elif len(detectors) == 3:
                ax1 = self.fig.add_subplot(221)
                ax2 = self.fig.add_subplot(222)
                ax3 = self.fig.add_subplot(223)

                self.multiPlotUtils(ax1, detectors[0])
                self.multiPlotUtils(ax2, detectors[1])
                self.multiPlotUtils(ax3, detectors[2])
            elif len(detectors) == 4:
                ax1 = self.fig.add_subplot(221)
                ax2 = self.fig.add_subplot(222)
                ax3 = self.fig.add_subplot(223)
                ax4 = self.fig.add_subplot(224)

                self.multiPlotUtils(ax1, detectors[0])
                self.multiPlotUtils(ax2, detectors[1])
                self.multiPlotUtils(ax3, detectors[2])
                self.multiPlotUtils(ax4, detectors[3])
            elif len(detectors) == 5:
                ax1 = self.fig.add_subplot(231)
                ax2 = self.fig.add_subplot(232)
                ax3 = self.fig.add_subplot(233)
                ax4 = self.fig.add_subplot(234)
                ax5 = self.fig.add_subplot(235)

                self.multiPlotUtils(ax1, detectors[0])
                self.multiPlotUtils(ax2, detectors[1])
                self.multiPlotUtils(ax3, detectors[2])
                self.multiPlotUtils(ax4, detectors[3])
                self.multiPlotUtils(ax5, detectors[4])
            elif len(detectors) == 6:
                ax1 = self.fig.add_subplot(231)
                ax2 = self.fig.add_subplot(232)
                ax3 = self.fig.add_subplot(233)
                ax4 = self.fig.add_subplot(234)
                ax5 = self.fig.add_subplot(235)
                ax6 = self.fig.add_subplot(236)

                self.multiPlotUtils(ax1, detectors[0])
                self.multiPlotUtils(ax2, detectors[1])
                self.multiPlotUtils(ax3, detectors[2])
                self.multiPlotUtils(ax4, detectors[3])
                self.multiPlotUtils(ax5, detectors[4])
                self.multiPlotUtils(ax6, detectors[5])
            elif len(detectors) == 7:
                ax1 = self.fig.add_subplot(331)
                ax2 = self.fig.add_subplot(332)
                ax3 = self.fig.add_subplot(333)
                ax4 = self.fig.add_subplot(334)
                ax5 = self.fig.add_subplot(335)
                ax6 = self.fig.add_subplot(336)
                ax7 = self.fig.add_subplot(337)

                self.multiPlotUtils(ax1, detectors[0])
                self.multiPlotUtils(ax2, detectors[1])
                self.multiPlotUtils(ax3, detectors[2])
                self.multiPlotUtils(ax4, detectors[3])
                self.multiPlotUtils(ax5, detectors[4])
                self.multiPlotUtils(ax6, detectors[5])
                self.multiPlotUtils(ax7, detectors[6])
            elif len(detectors) == 8:
                ax1 = self.fig.add_subplot(331)
                ax2 = self.fig.add_subplot(332)
                ax3 = self.fig.add_subplot(333)
                ax4 = self.fig.add_subplot(334)
                ax5 = self.fig.add_subplot(335)
                ax6 = self.fig.add_subplot(336)
                ax7 = self.fig.add_subplot(337)
                ax8 = self.fig.add_subplot(338)

                self.multiPlotUtils(ax1, detectors[0])
                self.multiPlotUtils(ax2, detectors[1])
                self.multiPlotUtils(ax3, detectors[2])
                self.multiPlotUtils(ax4, detectors[3])
                self.multiPlotUtils(ax5, detectors[4])
                self.multiPlotUtils(ax6, detectors[5])
                self.multiPlotUtils(ax7, detectors[6])
                self.multiPlotUtils(ax8, detectors[7])
            elif len(detectors) == 9:
                ax1 = self.fig.add_subplot(331)
                ax2 = self.fig.add_subplot(332)
                ax3 = self.fig.add_subplot(333)
                ax4 = self.fig.add_subplot(334)
                ax5 = self.fig.add_subplot(335)
                ax6 = self.fig.add_subplot(336)
                ax7 = self.fig.add_subplot(337)
                ax8 = self.fig.add_subplot(338)
                ax9 = self.fig.add_subplot(339)

                self.multiPlotUtils(ax1, detectors[0])
                self.multiPlotUtils(ax2, detectors[1])
                self.multiPlotUtils(ax3, detectors[2])
                self.multiPlotUtils(ax4, detectors[3])
                self.multiPlotUtils(ax5, detectors[4])
                self.multiPlotUtils(ax6, detectors[5])
                self.multiPlotUtils(ax7, detectors[6])
                self.multiPlotUtils(ax8, detectors[7])
                self.multiPlotUtils(ax9, detectors[8])
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

    def multiPlotUtils(self, ax, detector):
        """This method uses the pass axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :param detectorData: detector data from spec file
        :return:
        """
        if (len(self.selectedScans) > 0):
            for scan in self.selectedScans:
                detectorData = self.getSpecDetectorData(scan, detector)
                h, k, l = self.getHKL(detector)
                label = str(scan) + ": " + str(detector) + " -" + " H: " + str(h) + "," + " K: " + k + "," + " L: " + l
                xx, xLabel = self.getDetectorXAxis(scan)
                yy = detectorData
                ax.set_title(str(detector))
                ax.plot(xx, yy, label=str(label))
                ax.set_ylabel(str(detector))
                ax.set_xlabel(xLabel)

    def singlePlotUtils(self, ax, detector):
        """This method uses the pass axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :param detectorData: detector data from spec file
        :return:
        """
        if (len(self.selectedScans) > 0):
            for scan in self.selectedScans:
                detectorData = self.getSpecDetectorData(scan, detector)
                h, k, l = self.getHKL(detector)
                label = str(scan) + ": " + str(detector) + " -" + " H: " + str(h) + "," + " K: " + k + "," + " L: " + l
                xx, xLabel = self.getDetectorXAxis(scan)
                print(len(xx))
                yy = detectorData

                ax.plot(xx, yy, label=str(label))
                ax.set_ylabel(str(detector))
                ax.set_xlabel(xLabel)







