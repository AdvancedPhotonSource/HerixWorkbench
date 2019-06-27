#!/usr/bin/env python

"""
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.
"""
# -------------------------------------------Imports-------------------------------------------------------------------#
from __future__ import unicode_literals

import PyQt5.QtCore as qtCore
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtGui as qtGui
from matplotlib.pylab import plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from HerixWorkbench.tools.fit_dialog import FitDialog
# ----------------------------------------End of Imports---------------------------------------------------------------#


class Plot(qtWidgets.QWidget):
    """Creates the plot widget with its tabbed legend.
    """

    def __init__(self, parent=None):
        super(Plot, self).__init__(parent)
        self.mainWindow = parent

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.graphNavigationBar = NavigationToolbar(self.canvas, parent)
        self.legendList = PlotLegendList()
        self.defaultPlot()

        #  Current selected scans, detectors and counters
        self.detectors = []
        self.scans = []
        self.counters = []
        self.currentTab = 0

        # Adds the plotting widgets to the layout
        splitter = qtWidgets.QSplitter()
        splitter.setOrientation(qtCore.Qt.Vertical)
        splitter.addWidget(self.graphNavigationBar)
        splitter.addWidget(self.canvas)
        splitter.addWidget(self.legendList)

        # Adds the splitter as the layout of the widget
        layout = qtWidgets.QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

    def defaultPlot(self):
        self.clearPlot()
        axes = self.fig.add_subplot(111)
        axes.plot([1, 2, 3, 4], [1, 2, 3, 4])
        self.fig.tight_layout(rect=[0 , .04, 1, 1])
        self.canvas.draw()
        self.legendList.defaultLegend()

    def clearPlot(self):
        """Clears the plot"""
        self.fig.clear()
        self.canvas.draw()
        self.legendList.clearLegend()

    def singlePlot(self, detectors, scans):
        """This is the single plot that contains everything getting graphed.
        :param detectors: list of checked detectors
        :return:
        """
        self.clearPlot()
        self.detectors = detectors
        self.scans = scans

        if len(detectors) == 0 or len(scans) == 0:
            self.defaultPlot()
            return

        ax = self.fig.add_subplot(111)
        ax.set_ylabel("Analyzer Data")

        for scan in scans:
            self.singlePlotUtils(ax, scan, detectors)

        self.fig.tight_layout()
        self.canvas.draw()

    def singlePlotUtils(self, ax, scan, detectors):
        """This method uses the axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :return:
        """
        temp1, temp2 = scan.getTemp()
        legendLayout = self.legendList.create_legend(temp1, temp2)
        legendTitle = str(scan.getSpecFileName()) + " " + str(scan.getScanNumber())
        for d in detectors:
            detectorData = scan.getSpecDetectorData(d)
            xx, xLabel = scan.getDetectorXAxis()
            yy = detectorData
            if xx is None or yy is None:
                return
            h, k, l, diam = scan.getPlotLegendInfo(d)
            print("Value: ", scan.plotShifter.value())
            if scan.plotShifter.value() is not 0:
                xx = np.add(xx, scan.plotShifter.value())

            maximum = max(yy)
            maxIndx = yy.index(maximum)
            maxPos = xx[maxIndx]

            label = str(d) + " " + str(scan.getSpecFileName()) + " " + str(scan.getScanNumber())
            plot = ax.plot(xx, yy, label=label)
            ax.set_xlabel(xLabel)
            ax.legend(loc='upper right', fancybox=True, shadow=True, fontsize="x-small")

            self.legendList.add_legend(h, k, l, diam, maximum, maxPos, legendLayout, d)

        self.legendList.add_tab(legendLayout, legendTitle)

    def multiPlot(self, detectors, scans):
        self.clearPlot()
        self.detectors = detectors
        self.scans = scans

        if len(detectors) == 0 or len(scans) == 0:
            self.defaultPlot()
            return

        axes = []
        if len(detectors) == 1:
            ax1 = self.fig.add_subplot(111)
            axes.append(ax1)

        elif len(detectors) == 2:
           ax1 = self.fig.add_subplot(121)
           axes.append(ax1)
           ax2 = self.fig.add_subplot(122)
           axes.append(ax2)

        elif len(detectors) == 3:
            ax1 = self.fig.add_subplot(221)
            axes.append(ax1)
            ax2 = self.fig.add_subplot(222)
            axes.append(ax2)
            ax3 = self.fig.add_subplot(223)
            axes.append(ax3)

        elif len(detectors) == 4:
            ax1 = self.fig.add_subplot(221)
            axes.append(ax1)
            ax2 = self.fig.add_subplot(222)
            axes.append(ax2)
            ax3 = self.fig.add_subplot(223)
            axes.append(ax3)
            ax4 = self.fig.add_subplot(224)
            axes.append(ax4)

        elif len(detectors) == 5:
            ax1 = self.fig.add_subplot(231)
            axes.append(ax1)
            ax2 = self.fig.add_subplot(232)
            axes.append(ax2)
            ax3 = self.fig.add_subplot(233)
            axes.append(ax3)
            ax4 = self.fig.add_subplot(234)
            axes.append(ax4)
            ax5 = self.fig.add_subplot(235)
            axes.append(ax5)

        elif len(detectors) == 6:
            ax1 = self.fig.add_subplot(231)
            axes.append(ax1)
            ax2 = self.fig.add_subplot(232)
            axes.append(ax2)
            ax3 = self.fig.add_subplot(233)
            axes.append(ax3)
            ax4 = self.fig.add_subplot(234)
            axes.append(ax4)
            ax5 = self.fig.add_subplot(235)
            axes.append(ax5)
            ax6 = self.fig.add_subplot(236)
            axes.append(ax6)

        elif len(detectors) == 7:
            ax1 = self.fig.add_subplot(331)
            axes.append(ax1)
            ax2 = self.fig.add_subplot(332)
            axes.append(ax2)
            ax3 = self.fig.add_subplot(333)
            axes.append(ax3)
            ax4 = self.fig.add_subplot(334)
            axes.append(ax4)
            ax5 = self.fig.add_subplot(335)
            axes.append(ax5)
            ax6 = self.fig.add_subplot(336)
            axes.append(ax6)
            ax7 = self.fig.add_subplot(337)
            axes.append(ax7)

        elif len(detectors) == 8:
            ax1 = self.fig.add_subplot(331)
            axes.append(ax1)
            ax2 = self.fig.add_subplot(332)
            axes.append(ax2)
            ax3 = self.fig.add_subplot(333)
            axes.append(ax3)
            ax4 = self.fig.add_subplot(334)
            axes.append(ax4)
            ax5 = self.fig.add_subplot(335)
            axes.append(ax5)
            ax6 = self.fig.add_subplot(336)
            axes.append(ax6)
            ax7 = self.fig.add_subplot(337)
            axes.append(ax7)
            ax8 = self.fig.add_subplot(338)
            axes.append(ax8)

        elif len(detectors) >= 9:
            ax1 = self.fig.add_subplot(331)
            axes.append(ax1)
            ax2 = self.fig.add_subplot(332)
            axes.append(ax2)
            ax3 = self.fig.add_subplot(333)
            axes.append(ax3)
            ax4 = self.fig.add_subplot(334)
            axes.append(ax4)
            ax5 = self.fig.add_subplot(335)
            axes.append(ax5)
            ax6 = self.fig.add_subplot(336)
            axes.append(ax6)
            ax7 = self.fig.add_subplot(337)
            axes.append(ax7)
            ax8 = self.fig.add_subplot(338)
            axes.append(ax8)
            ax9 = self.fig.add_subplot(339)
            axes.append(ax9)

        for scan in scans:
            self.multi_plot_utils(axes, detectors, scan)

        self.fig.tight_layout(rect=[0, 0.1, 1, 1])
        self.canvas.draw()

    def multi_plot_utils(self, axes, detectors, scan):
        temp1, temp2 = scan.getTemp()
        legendLayout = self.legendList.create_legend(temp1, temp2)
        legendTitle = str(scan.getSpecFileName()) + " " + str(scan.getScanNumber())

        xx, xLabel = scan.getDetectorXAxis()
        if scan.plotShifter.value() is not 0:
            xx = np.add(xx, scan.plotShifter.value())

        for i in range(0, len(detectors)):
            if i == 9:
                break

            detector = detectors[i]
            ax = axes[i]
            yy = scan.getSpecDetectorData(detector)

            if xx is None or yy is None:
                return

            h, k, l, diam = scan.getPlotLegendInfo(detector)
            print("Value: ", scan.plotShifter.value())

            maximum = max(yy)
            maxIndx = yy.index(maximum)
            maxPos = xx[maxIndx]

            label = str(detector) + " " + str(scan.getSpecFileName()) + " " + str(scan.getScanNumber())
            plot = ax.plot(xx, yy, label=label)
            ax.set_xlabel(xLabel)
            ax.legend(loc='upper right', fancybox=True, shadow=True, fontsize="x-small")

            self.legendList.add_legend(h, k, l, diam, maximum, maxPos, legendLayout, detector)

        self.legendList.add_tab(legendLayout, legendTitle)


    def counterPlot(self, counters, scans):
        """
        :param counters: counters to be plot
        :param scans: scans to be plot
        :return:
        """
        self.counters = counters
        self.scans = scans
        self.clearPlot()
        self.legendList.setFixedHeight(0)

        if len(counters) == 0:
            self.defaultPlot()
        else:
            xCounter, yCounter, normalizer = counters
            ax = self.fig.add_subplot(111)
            ax.set_ylabel("Detector Data")
            ax.set_xlabel("Points")
            self.counterPlotUtils(ax, scans, xCounter, yCounter, normalizer)
            self.fig.tight_layout()
            self.canvas.draw()

    def counterPlotUtils(self, ax, scans, xCounter, yCounter, normalizer):
        if len(scans) > 0:
            for scan in scans:
                xx = scan.getSpecDetectorData(xCounter)
                yy = scan.getSpecDetectorData(yCounter)

                if xx is None or yy is None:
                    return

                if xx is None or yy is None:
                    qtWidgets.QMessageBox.warning(None, "Error",
                                                  "The data you are trying to plot cannot be found in " +
                                                  scan.getSpecFileName() + " scan " + scan.getScanNumber())
                    break

                maximum = max(yy)
                maxIndx = yy.index(maximum)
                maxPos = xx[maxIndx]
                scan.maxPos = maxPos
                scan.max = maximum

                if normalizer.find("PyQt") == -1:
                    mon = scan.getSpecDetectorData(normalizer)
                    yy = np.divide(yy, mon)

                if scan.plotShifter.value() is not 0:
                    xx = np.add(xx, scan.plotShifter.value())

                label = (str(scan.getSpecFileName()) + " " + str(scan.getScanNumber()))
                plot = ax.plot(xx, yy, label=label)
                ax.set_ylabel(yCounter)
                ax.set_xlabel(xCounter)

            ax.legend(loc='upper right', fancybox=True, shadow=True, fontsize="x-small")

    def show_fit_dialog(self):
        if len(self.detectors) == 0 or len(self.scans) == 0:
            return

        self.fit_dialog = FitDialog()
        numPeaks = self.fit_dialog.num_peaks.currentText()
        fitType = self.fit_dialog.fit_type.currentText()

        if self.fit_dialog.result() == 0:
            return

        self.clearPlot()
        ax = self.fig.add_subplot(111)
        ax.set_ylabel("Analyzer Data")

        for scan in self.scans:
            self.fitPlotUtils(ax, scan, self.detectors)

        self.fig.tight_layout()
        self.canvas.draw()


    def fitPlotUtils(self, ax, scan, detectors):
        """This method uses the axes and data to create the plot.
        :param ax: figure axes
        :param detector: detector name
        :return:
        """
        temp1, temp2 = scan.getTemp()
        fitType = self.fit_dialog.fit_type.currentText()
        legendLayout = self.legendList.create_legend(temp1, temp2)
        legendTitle = str(scan.getSpecFileName()) + " " + str(scan.getScanNumber())
        xx, xLabel = scan.getDetectorXAxis()
        for d in detectors:
            yy = scan.getSpecDetectorData(d)

            if xx is None or yy is None:
                return

            fittedData = self.fit_dialog.fit(xx, yy, fitType)
            if fittedData == []:
                return
            h, k, l, diam = scan.getPlotLegendInfo(d)

            if scan.plotShifter.value() is not 0:
                xx = np.add(xx, scan.plotShifter.value())

            maximum = max(yy)
            maxIndx = yy.index(maximum)
            maxPos = xx[maxIndx]

            label = str(d) + " " + str(scan.getSpecFileName()) + " " + str(scan.getScanNumber())
            plot = ax.plot(xx, yy, label=label)
            fitLabel = str(d) + " " + fitType
            ax.plot(xx, fittedData, 'ro:', label=fitLabel)
            ax.set_xlabel(xLabel)
            ax.legend(loc='upper right', fancybox=True, shadow=True, fontsize="x-small")

            self.legendList.add_legend(h, k, l, diam, maximum, maxPos, legendLayout, d)

        self.legendList.add_tab(legendLayout, legendTitle)

class PlotLegendList(qtWidgets.QTabWidget):
    """It uses a QListWidget to display the legend information."""

    def __init__(self):
        super(PlotLegendList, self).__init__()
        self.setFixedHeight(130)
        self.defaultLegend()

    def create_legend(self, Tval1, Tval2):
        self.setFixedHeight(130)
        vLayout = qtWidgets.QVBoxLayout()
        tLayout = qtWidgets.QHBoxLayout()

        tempLbl = qtWidgets.QLabel("Temp:")

        temp1 = qtWidgets.QLabel(str(Tval1))
        temp2 = qtWidgets.QLabel(str(Tval2))

        tLayout.addWidget(tempLbl)
        tLayout.addWidget(temp1)
        tLayout.addWidget(temp2)
        tLayout.addStretch(1)
        tLayout.addStretch(1)

        vLayout.addLayout(tLayout)

        return vLayout

    def add_legend(self, h, k, l, diamVal, peakVal, pos, vLayout, detector):
        hLayout = qtWidgets.QHBoxLayout()

        # Creating the widgets for the legend
        detLbl = qtWidgets.QLabel(detector + " - ")

        hLbl = qtWidgets.QLabel("H:")
        H = qtWidgets.QLineEdit()
        H.setReadOnly(True)

        kLbl = qtWidgets.QLabel("K:")
        K = qtWidgets.QLineEdit()
        K.setReadOnly(True)

        lLbl = qtWidgets.QLabel("L:")
        L = qtWidgets.QLineEdit()
        L.setReadOnly(True)

        diamLbl = qtWidgets.QLabel("Diam:")
        diam = qtWidgets.QLineEdit()
        diam.setReadOnly(True)

        peakLbl = qtWidgets.QLabel("Peak:")
        peak = qtWidgets.QLineEdit()
        peak.setReadOnly(True)

        positionLbl = qtWidgets.QLabel("Position:")
        position = qtWidgets.QLineEdit()
        position.setReadOnly(True)

        widthLbl = qtWidgets.QLabel("Width:")
        width = qtWidgets.QLineEdit()
        width.setReadOnly(True)

        # Adding the widgets to the horizontal layout
        hLayout.addWidget(detLbl)
        hLayout.addWidget(hLbl)
        hLayout.addWidget(H)
        hLayout.addWidget(kLbl)
        hLayout.addWidget(K)
        hLayout.addWidget(lLbl)
        hLayout.addWidget(L)
        hLayout.addWidget(diamLbl)
        hLayout.addWidget(diam)
        hLayout.addWidget(peakLbl)
        hLayout.addWidget(peak)
        hLayout.addWidget(positionLbl)
        hLayout.addWidget(position)

        # Setting the values to the legend
        H.setText(str(h))
        K.setText(str(k))
        L.setText(str(l))
        diam.setText(str(diamVal))
        peak.setText(str(peakVal))
        position.setText(str(pos))

        vLayout.addLayout(hLayout)


    def add_tab(self, vLayout, title):
        scroll = qtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)

        legend = qtWidgets.QWidget(scroll)
        vLayout.addStretch(1)
        legend.setLayout(vLayout)

        scroll.setWidget(legend)
        self.addTab(scroll, title)

    def defaultLegend(self):
        self.clearLegend()
        legend = qtWidgets.QWidget()
        self.addTab(legend, "Default")
        self.setFixedHeight(0)

    def clearLegend(self):
        if self.count() > 0:
            for i in range(self.count()):
                self.removeTab(0)