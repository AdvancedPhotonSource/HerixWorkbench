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


class ANAContainer(QWidget):
    """Creates the group box with the detector check boxes."""

    # Signals
    detectorsSelected = pyqtSignal(list, name="detectorSelected")

    def __init__(self, parent=None):
        super(ANAContainer, self).__init__(parent)
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
        hBox3 = QHBoxLayout()
        hBox3.addWidget(QWidget())

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.setExclusive(False)

        # Detectors Ana1 - Ana3
        for i in range(1, 4):
            checkBox = QCheckBox("Ana" + str(i))
            self.buttonGroup.addButton(checkBox, i)
            hBox0.addWidget(checkBox)
            self.detectorCheckBoxes.append(checkBox)
            checkBox.stateChanged.connect(self.detectorCheckBoxState)

        # Detectors Ana4-Ana6
        for i in range(4, 7):
            checkBox = QCheckBox("Ana" + str(i))
            self.buttonGroup.addButton(checkBox, i)
            hBox1.addWidget(checkBox)
            self.detectorCheckBoxes.append(checkBox)
            checkBox.stateChanged.connect(self.detectorCheckBoxState)

        # Detectors Ana7-Ana9
        for i in range(7, 10):
            checkBox = QCheckBox("Ana" + str(i))
            self.buttonGroup.addButton(checkBox, i)
            hBox2.addWidget(checkBox)
            self.detectorCheckBoxes.append(checkBox)
            checkBox.stateChanged.connect(self.detectorCheckBoxState)

        # PIN_C Detector
        checkBox = QCheckBox("PIN-C")
        self.buttonGroup.addButton(checkBox, 10)
        hBox3.addWidget(checkBox)
        self.detectorCheckBoxes.append(checkBox)
        checkBox.stateChanged.connect(self.detectorCheckBoxState)

        # All-Detector Checkbox
        checkBox = QCheckBox("Select All")
        self.buttonGroup.addButton(checkBox, 11)
        hBox3.addWidget(checkBox)
        self.detectorCheckBoxes.append(checkBox)
        checkBox.stateChanged.connect(self.selectAllDetectorsState)


        vBox.addLayout(hBox0)
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox3)

        self.detectorGroupBx.setLayout(vBox)

    def detectorCheckBoxState(self, i):
        """Emits a signal containing the list of the checked boxes when the state of one check box
        has changed
        """
        checkedDetectors = []
        for i in range(0, 9):
            if self.detectorCheckBoxes[i].checkState() == 2:
                checkedDetectors.append("Ana"+str(i+1))

        if self.detectorCheckBoxes[9].checkState() == 2:
            checkedDetectors.append("PIN-C")

        self.detectorSelected[list].emit(checkedDetectors)

    def selectAllDetectorsState(self):
        """Checks if the Select All checkbox is checked. If it is,
        it makes sure the PIN-C detector is unchecked  and selected
        the ANA detectors, else, it unchecks all the ANA detectors
        """

        if self.detectorCheckBoxes[10].checkState() == 2:
            self.disconnectDetectorCheckBoxState()
            self.detectorCheckBoxes[9].setCheckState(Qt.Unchecked)
            for i in range(0, 9):
                self.detectorCheckBoxes[i].setCheckState(Qt.Checked)
            self.connectDetectorCheckBoxState()
            self.detectorCheckBoxState(1)
        else:
            self.disconnectDetectorCheckBoxState()
            for i in range(0, 10):
                self.detectorCheckBoxes[i].setCheckState(Qt.Unchecked)

            self.connectDetectorCheckBoxState()
            self.detectorCheckBoxState(1)

    def disconnectDetectorCheckBoxState(self):
        """Disconnects the detectors check boxes from the
        detectorCheckBoxState method
        """
        for i in range(0, 10):
            self.detectorCheckBoxes[i].stateChanged.disconnect(self.detectorCheckBoxState)

    def connectDetectorCheckBoxState(self):
        for i in range(0, 10):
            self.detectorCheckBoxes[i].stateChanged.connect(self.detectorCheckBoxState)