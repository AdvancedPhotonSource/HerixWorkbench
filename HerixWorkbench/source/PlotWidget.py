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

    def SinglePlot(self):
        pass

    def MultiPlot(self):
        pass


