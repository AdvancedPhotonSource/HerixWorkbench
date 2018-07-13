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
from PyQt5.QtGui import *
from HerixWorkbench.tools.scanbrowser import ScanBrowser
# ---------------------------------------------------------------------------------------------------------------------#


class SpecDataSelector(QTabWidget):
    """Main window class"""
    def __init__(self, parent=None):
        super(SpecDataSelector, self).__init__(parent)
        self.scanBrowserArray = []
        self.defaultScanBrowser()
        self.isDefaultBrowserOn = True

    def defaultScanBrowser(self):
        if self.count() > 0:
            for i in range(self.count()):
                self.removeTab(i)
                self.scanBrowserArray.pop(i)

        self.addTab(ScanBrowser(), "Default")
        self.isDefaultBrowserOn = True

    def addScanBrowser(self, specFileName):
        if self.isDefaultBrowserOn is True:
            self.removeTab(0)
            self.isDefaultBrowserOn = False

        scanBrowser = ScanBrowser()
        self.scanBrowserArray.append(scanBrowser)
        self.addTab(scanBrowser, str(specFileName))
