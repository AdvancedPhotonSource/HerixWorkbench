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
from HerixWorkbench.widgets.scan_browser import ScanBrowser
# ---------------------------------------------------------------------------------------------------------------------#


class ScanBrowserPicker(QTabWidget):
    """Main window class"""
    def __init__(self, parent=None):
        super(ScanBrowserPicker, self).__init__(parent)
        self.defaultScanBrowser()
        self.isDefaultBrowserOn = True

        #  Keeps track of the spec files
        self.specFileInPicker = []

    def defaultScanBrowser(self):
        self.addTab(ScanBrowser(), "Default")
        self.isDefaultBrowserOn = True

    def addScanBrowser(self, specFile):
        if self.isDefaultBrowserOn is True:
            self.removeTab(0)
            self.isDefaultBrowserOn = False

        self.specFileInPicker.append(specFile)
        scanBrowser = specFile.scanBrowser
        self.addTab(scanBrowser, specFile.getSpecFileName())

    def removeSpecFileScanBrowser(self, specFile):
        for i in range(len(self.specFileInPicker)):
            if specFile == self.specFileInPicker[i]:
                self.removeTab(i)
                self.specFileInPicker.pop(i)
                break

        if self.count() == 0:
            self.defaultScanBrowser()

