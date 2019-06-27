#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals
import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
import numpy as np

from lmfit.models import GaussianModel, VoigtModel, LorentzianModel, LinearModel


import os
# ---------------------------------------------------------------------------------------------------------------------#

class FitDialog(qtWidgets.QDialog):

    def __init__(self):
        super(FitDialog, self).__init__()
        self.setWindowTitle("Choose Fit")
        self.setBaseSize(300, 250)

        self.do_fit = False

        #  Dialog widgets
        self.fit_type = qtWidgets.QComboBox()
        self.fit_type.addItem("Gaussian")
        self.fit_type.addItem("Lorentzian")
        self.fit_type.addItem("Voigt")

        self.num_peaks = qtWidgets.QComboBox()
        self.num_peaks.addItem("One")

        okayBtn = qtWidgets.QPushButton("Okay")
        okayBtn.pressed.connect(self.accept)

        cancelBtn = qtWidgets.QPushButton("Cancel")
        cancelBtn.pressed.connect(self.reject)

        #  Layout of widgets
        gridLyt = qtWidgets.QGridLayout()
        gridLyt.addWidget(qtWidgets.QLabel("Choose fit type:"), 0, 0, 1, 2)
        gridLyt.addWidget(self.fit_type, 1, 0, 1, 2)
        gridLyt.addWidget(qtWidgets.QLabel("Choose number of peaks:"), 2, 0, 1, 2)
        gridLyt.addWidget(self.num_peaks, 3, 0, 1, 2)
        gridLyt.addItem(qtWidgets.QSpacerItem(15,15), 4, 0, 1, 2)
        gridLyt.addWidget(cancelBtn, 5, 0)
        gridLyt.addWidget(okayBtn, 5, 1)
        self.setLayout(gridLyt)

        self.exec_()

    def fit(self, xx, yy, fitType):
        xx = np.asarray(xx)
        yy = np.asarray(yy)
        print("XX",xx)
        print("YY", yy)
        print(len(xx))
        print(len(yy))
        print("XX", xx)
        x1 = xx[0]
        x2 = xx[-1]
        y1 = yy[0]
        y2 = yy[-1]
        m = (y2 - y1) / (x2 - x1)
        b = y2 - m * x2

        if fitType == "Gaussian":
            mod = GaussianModel()
        elif fitType == "Lorentzian":
            mod = LorentzianModel()
        else:
            mod = VoigtModel()

        pars = mod.guess(yy, x=xx, slope=m)
        print(pars)
        mod = mod + LinearModel()
        pars.add('intercept', value=b, vary=True)
        pars.add('slope', value=m, vary=True)
        out = mod.fit(yy, pars, x=xx)

        return out.best_fit