"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

import sys

import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from lmfit.models import VoigtModel, LinearModel
# ---------------------------------------------------------------------------------------------------------------------#

class FitDialog(qtWidgets.QDialog):

    def __init__(self, parent=None):
        super(FitDialog, self).__init__(parent)
        self.data = ""
        self.numberOfPeaks = qtWidgets.QLineEdit()
        self.voigtFitBtn = qtWidgets.QPushButton("Voigt Fit")
        self.voigtFitBtn.pressed.connect(self.voigtFit)

        vLayout = qtWidgets.QVBoxLayout()
        #vLayout.addWidget(self.numberOfPeaks)
        vLayout.addWidget(self.voigtFitBtn)
        self.setWindowTitle("Voigt Fit")
        self.setLayout(vLayout)

    def setData(self, data):
        self.data = data
        print("Data: \n", data)
        self.exec_()

    def voigtFit(self):
        numPeaks = int(self.numberOfPeaks.text())
        self.getVoigFit(self.data)


    def fitWindow(self, xx, yy):
        try:
            self.mainGraph = qtWidgets.QDialog()
            self.mainGraph.resize(600, 600)
            dpi = 100
            fig = Figure((3.0, 3.0), dpi=dpi)
            canvas = FigureCanvas(fig)
            canvas.setParent(self.mainGraph)
            axes = fig.add_subplot(111)

            axes.plot(xx, yy, 'b+:', label='data')

            axes.legend()
            axes.set_xlabel('Bins')
            axes.set_ylabel('Fit')
            canvas.draw()

            vbox = qtWidgets.QVBoxLayout()
            hbox = qtWidgets.QHBoxLayout()
            self.skipEachFitGraphButton()
            self.nextFitGraphButton()
            hbox.addWidget(self.skipEachFitGraphBtn)
            hbox.addStretch(1)
            hbox.addWidget(self.nextFitGraphBtn)
            graphNavigationBar = NavigationToolbar(canvas, self.mainGraph)
            vbox.addLayout(hbox)
            vbox.addWidget(graphNavigationBar)
            vbox.addWidget(canvas)
            self.mainGraph.setLayout(vbox)
            self.mainGraph.exec_()
        except Exception as e:
            qtWidgets.QMessageBox.warning(self.myMainWindow, "Error",
                                "Please make sure the guesses are realistic when fitting. \n\n" + str(e))

    def getVoigFit(self, data):
        try:

            yy1 = []
            yy2 = []
            yy = data
            xx = range(0, len(yy))
            #m = (y2 - y1) / (x2 - x1)
            #b = y2 - m * x2
            """ i = 0
            for y in yy:
                if i < len(yy) / 2:
                    yy1.append(y)
                else:
                    yy2.append(y)
                i += 1

            xx = range(0, len(yy))
            xx1 = range(0, len(yy) / 2)
            xx2 = range(len(yy) / 2, len(yy))

            x1 = xx[0]
            x2 = xx[-1]
            y1 = yy[0]
            y2 = yy[-1]
            """

            mod1 = VoigtModel(prefix='p1_')

            pars1 = mod1.guess(yy, x=xx)
            mod = mod1 + LinearModel()
            pars = pars1

            pars.add('intercept')
            pars.add('slope', vary=False)

            out = mod.fit(yy, pars, x=xx)

            # Saves fitted data of each fit
            fitData = out.best_fit
            #binFit = np.reshape(fitData, (len(fitData), 1))

            self.fitWindow(xx, fitData)
            return False
        except Exception as e:
            qtWidgets.QMessageBox.warning("Error", "Something went wrong while fitting. \n\n" +
                                                            "The following exception occur: " + str(e))
            return True