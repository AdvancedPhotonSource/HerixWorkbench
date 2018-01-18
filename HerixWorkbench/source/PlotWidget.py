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
        #self.fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
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
            ax.set_title(str(self.specShortName()))
            ax.set_ylabel("Detector Data")
            ax.set_xlabel("Points")
            detectorData = self.getSpecDetectorData(detectors)
            for d in detectors:
                self.multiPlotUtils(ax, d, detectorData[str(d)])
            ax.legend()

            self.canvas.draw()

    def multiPlot(self, detectors):
        self.clearPlot()
        detectorData = self.getSpecDetectorData(detectors)

        if len(detectors) == 1:
            ax1 = self.fig.add_subplot(111)
            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
        elif len(detectors) == 2:
           ax1 = self.fig.add_subplot(121)
           ax2 = self.fig.add_subplot(122)

           self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
           self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
        elif len(detectors) == 3:
            ax1 = self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(222)
            ax3 = self.fig.add_subplot(223)

            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
            self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
            self.singlePlotUtils(ax3, detectors[2], detectorData[str(detectors[2])])
        elif len(detectors) == 4:
            ax1 = self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(222)
            ax3 = self.fig.add_subplot(223)
            ax4 = self.fig.add_subplot(224)

            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
            self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
            self.singlePlotUtils(ax3, detectors[2], detectorData[str(detectors[2])])
            self.singlePlotUtils(ax4, detectors[3], detectorData[str(detectors[3])])
        elif len(detectors) == 5:
            ax1 = self.fig.add_subplot(231)
            ax2 = self.fig.add_subplot(232)
            ax3 = self.fig.add_subplot(233)
            ax4 = self.fig.add_subplot(234)
            ax5 = self.fig.add_subplot(235)

            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
            self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
            self.singlePlotUtils(ax3, detectors[2], detectorData[str(detectors[2])])
            self.singlePlotUtils(ax4, detectors[3], detectorData[str(detectors[3])])
            self.singlePlotUtils(ax5, detectors[4], detectorData[str(detectors[4])])
        elif len(detectors) == 6:
            ax1 = self.fig.add_subplot(231)
            ax2 = self.fig.add_subplot(232)
            ax3 = self.fig.add_subplot(233)
            ax4 = self.fig.add_subplot(234)
            ax5 = self.fig.add_subplot(235)
            ax6 = self.fig.add_subplot(236)

            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
            self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
            self.singlePlotUtils(ax3, detectors[2], detectorData[str(detectors[2])])
            self.singlePlotUtils(ax4, detectors[3], detectorData[str(detectors[3])])
            self.singlePlotUtils(ax5, detectors[4], detectorData[str(detectors[4])])
            self.singlePlotUtils(ax6, detectors[5], detectorData[str(detectors[5])])
        elif len(detectors) == 7:
            ax1 = self.fig.add_subplot(331)
            ax2 = self.fig.add_subplot(332)
            ax3 = self.fig.add_subplot(333)
            ax4 = self.fig.add_subplot(334)
            ax5 = self.fig.add_subplot(335)
            ax6 = self.fig.add_subplot(336)
            ax7 = self.fig.add_subplot(337)

            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
            self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
            self.singlePlotUtils(ax3, detectors[2], detectorData[str(detectors[2])])
            self.singlePlotUtils(ax4, detectors[3], detectorData[str(detectors[3])])
            self.singlePlotUtils(ax5, detectors[4], detectorData[str(detectors[4])])
            self.singlePlotUtils(ax6, detectors[5], detectorData[str(detectors[5])])
            self.singlePlotUtils(ax7, detectors[6], detectorData[str(detectors[6])])
        elif len(detectors) == 8:
            ax1 = self.fig.add_subplot(331)
            ax2 = self.fig.add_subplot(332)
            ax3 = self.fig.add_subplot(333)
            ax4 = self.fig.add_subplot(334)
            ax5 = self.fig.add_subplot(335)
            ax6 = self.fig.add_subplot(336)
            ax7 = self.fig.add_subplot(337)
            ax8 = self.fig.add_subplot(338)

            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
            self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
            self.singlePlotUtils(ax3, detectors[2], detectorData[str(detectors[2])])
            self.singlePlotUtils(ax4, detectors[3], detectorData[str(detectors[3])])
            self.singlePlotUtils(ax5, detectors[4], detectorData[str(detectors[4])])
            self.singlePlotUtils(ax6, detectors[5], detectorData[str(detectors[5])])
            self.singlePlotUtils(ax7, detectors[6], detectorData[str(detectors[6])])
            self.singlePlotUtils(ax8, detectors[7], detectorData[str(detectors[7])])
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

            self.singlePlotUtils(ax1, detectors[0], detectorData[str(detectors[0])])
            self.singlePlotUtils(ax2, detectors[1], detectorData[str(detectors[1])])
            self.singlePlotUtils(ax3, detectors[2], detectorData[str(detectors[2])])
            self.singlePlotUtils(ax4, detectors[3], detectorData[str(detectors[3])])
            self.singlePlotUtils(ax5, detectors[4], detectorData[str(detectors[4])])
            self.singlePlotUtils(ax6, detectors[5], detectorData[str(detectors[5])])
            self.singlePlotUtils(ax7, detectors[6], detectorData[str(detectors[6])])
            self.singlePlotUtils(ax8, detectors[7], detectorData[str(detectors[7])])
            self.singlePlotUtils(ax9, detectors[8], detectorData[str(detectors[8])])
        else:
            self.defaultPlot()
        self.canvas.draw()
        self.fig.tight_layout()

    def clearPlot(self):
        """Clears the plot"""
        self.fig.clear()

    def singlePlotUtils(self, ax, detector, detectorData):
        """This method uses the pass axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :param detectorData: detector data from spec file
        :return:
        """
        xx = range(1, len(detectorData)+1)
        yy = detectorData
        ax.set_title(str(detector))
        ax.plot(xx, yy)
        ax.set_ylabel(str(detector))
        ax.set_xlabel("Points")

    def multiPlotUtils(self, ax, detector, detectorData):
        """This method uses the pass axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :param detectorData: detector data from spec file
        :return:
        """
        xx = range(1, len(detectorData) + 1)
        yy = detectorData
        ax.plot(xx, yy, label=str(detector))







