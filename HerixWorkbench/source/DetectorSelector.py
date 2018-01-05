#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# ----------------------------------------End of Imports---------------------------------------------------------------#

class SelectorContainer(QGroupBox):
    """Creates the group box with the detector check boxes."""

    # Signals
    detectorsSelected = pyqtSignal(list, name="detectorSelected")

    def __init__(self, parent=None):
        super(SelectorContainer, self).__init__(parent)
        self.setTitle("Detectors")
        self.detectorCheckBoxes = []
        self.createDetectorCheckBoxes()

    def createDetectorCheckBoxes(self):
        vBox = QVBoxLayout()
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(False)
        for i in range(1, 10):
            checkBox = QCheckBox("Ana" + str(i))
            self.buttonGroup.addButton(checkBox, i)
            vBox.addWidget(checkBox)
            self.detectorCheckBoxes.append(checkBox)
            checkBox.stateChanged.connect(self.detectorCheckBoxState)

        self.setLayout(vBox)

    def detectorCheckBoxState(self, i):
        checkedDetectors = []
        for i in range(0, 9):
            if self.detectorCheckBoxes[i].checkState() == 2:
                checkedDetectors.append(i+1)

        self.detectorSelected[list].emit(checkedDetectors)

