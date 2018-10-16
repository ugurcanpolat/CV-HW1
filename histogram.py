#!/usr/local/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog, qApp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()

        self.title = 'Histogram Equalization'

        self.initUI()

    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.
        return NotImplementedError

    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        return NotImplementedError

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        inputAct = QAction('Open input', self)
        inputAct.triggered.connect(self.openInputImage)

        targetAct = QAction('Open target', self) 
        targetAct.triggered.connect(self.openTargetImage)

        exitAct = QAction('Exit', self)        
        exitAct.triggered.connect(qApp.quit)

        fileMenu.addAction(inputAct)
        fileMenu.addAction(targetAct)
        fileMenu.addAction(exitAct)

        histogramAct = QAction('Equalize Histogram', self) 
        histogramAct.triggered.connect(self.histogramButtonClicked)
        
        toolbar = self.addToolBar('Histogram Equalization')
        toolbar.addAction(histogramAct)

        self.createEmptyInputGroupBox()
        self.createEmptyTargetGroupBox()
        self.createEmptyResultGroupBox()

        # Since QMainWindows layout has already been set, create central widget
        # to manipulate layout of main window
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Initialize input, target, result boxes
        windowLayout = QGridLayout()
        windowLayout.addWidget(self.inputGroupBox, 0, 0)
        windowLayout.addWidget(self.targetGroupBox, 0, 1)
        windowLayout.addWidget(self.resultGroupBox, 0, 2)
        wid.setLayout(windowLayout)

        self.setWindowTitle(self.title) 
        self.showMaximized()
        self.show()

    def createEmptyInputGroupBox(self):
        self.inputGroupBox = QGroupBox('Input')
        layout = QVBoxLayout()

        self.inputGroupBox.setLayout(layout)

    def createEmptyTargetGroupBox(self):
        self.targetGroupBox = QGroupBox('Target')
        layout = QVBoxLayout()

        self.targetGroupBox.setLayout(layout)

    def createEmptyResultGroupBox(self):
        self.resultGroupBox = QGroupBox('Result')
        layout = QVBoxLayout()

        self.resultGroupBox.setLayout(layout)

    def histogramButtonClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            return NotImplementedError
        if not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            return NotImplementedError
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            return NotImplementedError

    def calcHistogram(self, I):
        # Calculate histogram
        return NotImplementedError

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        return NotImplementedError
        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        return NotImplementedError
        # Plot histogram

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())