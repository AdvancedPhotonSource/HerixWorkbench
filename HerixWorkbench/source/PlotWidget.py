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
# ----------------------------------------End of Imports---------------------------------------------------------------#

class PlotWidget(QWidget):
    """Creates the group box with the detector check boxes."""

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)
        self.axes.plot([1,2,3,4], [1,2,3,4])
        self.canvas.draw()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def singlePlot(self):
        pass

    def multiPlot(self, detectors):
        self.clearPlot()
        if len(detectors) == 1:
            self.fig.add_subplot(111)
        elif len(detectors) == 2:
           ax1 = self.fig.add_subplot(121)
           ax2 = self.fig.add_subplot(122)
        elif len(detectors) == 3:
            ax1 = self.fig.add_subplot(221)
            ax2 = self.fig.add_subplot(222)
            ax2 = self.fig.add_subplot(223)
        self.canvas.draw()
        # adding legend
        # self.axes.legend(loc='bottom center', bbox_to_anchor=(1.45, .08), shadow=True, ncol=1)
        pass

    def clearPlot(self):
        self.fig.clear()


