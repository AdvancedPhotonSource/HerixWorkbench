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


class ScanDataSelector(QTabWidget):
    """Main window class"""
    def __init__(self, parent=None):
        super(ScanDataSelector, self).__init__(parent)
        self.scanBrowserArray = []
        self.defaultScanBrowser()
        self.isDefaultBrowserOn = True

    def defaultScanBrowser(self):
        print(" Default Browser: ")
        print(self.count())
        print(self.scanBrowserArray)
        if self.count() > 0:
            for i in range(self.count()):
                self.removeTab(0)
                self.scanBrowserArray.pop(0)

        self.addTab(ScanBrowser(), "Default")
        self.isDefaultBrowserOn = True

    def addScanBrowser(self, specFileName):
        if self.isDefaultBrowserOn is True:
            self.removeTab(0)
            self.isDefaultBrowserOn = False

        scanBrowser = ScanBrowser()
        self.scanBrowserArray.append(scanBrowser)
        self.addTab(scanBrowser, str(specFileName))
