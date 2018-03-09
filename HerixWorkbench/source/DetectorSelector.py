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

class SelectorContainer(QWidget):
    """Creates the group box with the detector check boxes."""

    # Signals
    detectorsSelected = pyqtSignal(list, name="detectorSelected")

    def __init__(self, parent=None):
        super(SelectorContainer, self).__init__(parent)
        self.detectorGroupBx = QGroupBox()
        hLayout = QHBoxLayout()
        self.detectorGroupBx.setTitle("Detectors")
        self.detectorCheckBoxes = []
        self.createDetectorCheckBoxes()
        hLayout.addWidget(self.detectorGroupBx)
        self.setLayout(hLayout)

    def createDetectorCheckBoxes(self):
        """Initializes the nine check boxes and adds them to the QGroupBox
        :return:
        """
        vBox = QVBoxLayout()
        hBox0 = QHBoxLayout()
        hBox1 = QHBoxLayout()
        hBox2 = QHBoxLayout()
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(False)
        for i in range(1, 4):
            checkBox = QCheckBox("Ana" + str(i))
            self.buttonGroup.addButton(checkBox, i)
            hBox0.addWidget(checkBox)
            self.detectorCheckBoxes.append(checkBox)
            checkBox.stateChanged.connect(self.detectorCheckBoxState)

        for i in range(4, 7):
            checkBox = QCheckBox("Ana" + str(i))
            self.buttonGroup.addButton(checkBox, i)
            hBox1.addWidget(checkBox)
            self.detectorCheckBoxes.append(checkBox)
            checkBox.stateChanged.connect(self.detectorCheckBoxState)

        for i in range(7, 10):
            checkBox = QCheckBox("Ana" + str(i))
            self.buttonGroup.addButton(checkBox, i)
            hBox2.addWidget(checkBox)
            self.detectorCheckBoxes.append(checkBox)
            checkBox.stateChanged.connect(self.detectorCheckBoxState)

        vBox.addLayout(hBox0)
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)

        self.detectorGroupBx.setLayout(vBox)

    def detectorCheckBoxState(self, i):
        """Emits a signal containing the list of the checked boxes when the state of one check box
        has changed. """
        checkedDetectors = []
        for i in range(0, 9):
            if self.detectorCheckBoxes[i].checkState() == 2:
                checkedDetectors.append(i+1)

        self.detectorSelected[list].emit(checkedDetectors)

