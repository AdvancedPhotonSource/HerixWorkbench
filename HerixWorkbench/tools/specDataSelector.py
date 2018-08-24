#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# ---------------------------------------------------------------------------------------------------------------------#
from __future__ import unicode_literals

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from HerixWorkbench.tools.DetectorSelector import SelectorContainer
from specguiutils.counterselector import CounterSelector

COUNTER_OPTS = ["X", "Y", "Mon"]
# ---------------------------------------------------------------------------------------------------------------------#


class SpecDataSelector(QTabWidget):
    """Main window class"""

    # Signals
    detectorsSelected = pyqtSignal(list, name="detectorSelected")
    countersSelected = pyqtSignal(list, name="countersSelected")
    tabChanged = pyqtSignal(int, name="tabChanged")

    def __init__(self, parent=None):
        super(SpecDataSelector, self).__init__(parent)
        self.counterSelector = CounterSelector(counterOpts=COUNTER_OPTS)
        self.counterSelector.counterView.counterDataChanged.connect(self.newCounterSelected)
        self.selectorContainer = SelectorContainer()
        self.selectorContainer.detectorsSelected.connect(self.anaDetectorSelected)
        self.currentChanged.connect(self.newTabChanged)

        self.addTab(self.counterSelector, "Spec Data")
        self.addTab(self.selectorContainer, "Analyzers")

    def anaDetectorSelected(self, detectors):
        self.detectorsSelected[list].emit(detectors)

    def loadCounters(self, scanLabels):
        self.counterSelector.counterModel.initializeDataRows(COUNTER_OPTS, scanLabels)
        self.counterSelector.counterModel.setCounterOptions(COUNTER_OPTS)
        self.counterSelector.setSelectedCounters(["", ""])
        self.newCounterSelected(self.counterSelector.getSelectedCounters())

    def newCounterSelected(self, counters):
        countersNames = self.counterSelector.getSelectedCounterNames(counters)
        self.countersSelected[list].emit(countersNames)

    def newTabChanged(self, index):
        self.tabChanged[int].emit(index)
