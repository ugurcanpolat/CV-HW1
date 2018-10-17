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

        self.inputLoaded = False
        self.targetLoaded = False
        self.resultLoaded = False

        self.setFixedSize(self.geometry().width(), self.geometry().height())

        self.initUI()

    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.

        fName = QFileDialog.getOpenFileName(self, 'Open input file', './', 'Image files (*.png *.jpg)')

        if fName[0] == '':
            return

        if self.inputLoaded:
            self.deleteItemsFromWidget(self.inputGroupBox.layout())

        if self.resultLoaded:
            self.deleteItemsFromWidget(self.targetGroupBox.layout())

        self.inputImage = cv2.imread(fName[0])

        height, width, channel = self.inputImage.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.inputImage.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        self.inputLoaded = True
        pix = QPixmap(qImg)

        w = self.inputGroupBox.width()
        h = self.inputGroupBox.height() / 2

        label = QLabel('Input image')
        label.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio))
        label.setAlignment(Qt.AlignCenter)
        self.inputGroupBox.layout().addWidget(label)

    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        fName = QFileDialog.getOpenFileName(self, 'Open target file', './', 'Image files (*.png *.jpg)')

        if fName[0] == '':
            return

        if self.targetLoaded:
            self.deleteItemsFromWidget(self.targetGroupBox.layout())

        if self.resultLoaded:
            self.deleteItemsFromWidget(self.targetGroupBox.layout())

        self.targetImage = cv2.imread(fName[0])

        height, width, channel = self.targetImage.shape
        bytesPerLine = 3 * width
        qImg = QImage(self.targetImage.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        self.targetLoaded = True
        pix = QPixmap(qImg)

        w = self.targetGroupBox.width()
        h = self.targetGroupBox.height() / 2

        label = QLabel('Target image')
        label.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio))
        label.setAlignment(Qt.AlignCenter)
        self.targetGroupBox.layout().addWidget(label)

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
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input and target images are missing.")
            msg.setText('First load input and target images!')
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()
        elif not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input image is missing.")
            msg.setText('Load input image!')
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Target image is missing.")
            msg.setText('Load target image!')
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec()

    def calcHistogram(self, I):
        # Calculate histogram
        return NotImplementedError

    def deleteItemsFromWidget(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    deleteItemsFromWidget(item.layout())

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