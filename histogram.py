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

        if fName[0] is '':
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

        self.inputHistogram = self.calcHistogram(self.inputImage)
        canvas = PlotCanvas(self.inputHistogram, height=h/100, width=w/100)

        label = QLabel('Input image')
        label.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio))
        label.setAlignment(Qt.AlignCenter)
        self.inputGroupBox.layout().addWidget(label)
        self.inputGroupBox.layout().addWidget(canvas)

    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        fName = QFileDialog.getOpenFileName(self, 'Open target file', './', 'Image files (*.png *.jpg)')

        if fName[0] is '':
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

        self.targetHistogram = self.calcHistogram(self.targetImage)
        canvas = PlotCanvas(self.targetHistogram, height=h/100, width=w/100)

        label = QLabel('Target image')
        label.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio))
        label.setAlignment(Qt.AlignCenter)
        self.targetGroupBox.layout().addWidget(label)
        self.targetGroupBox.layout().addWidget(canvas)

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

        matched = HistogramMatcher(self.inputImage, self.inputHistogram, self.targetImage, self.targetHistogram)
        self.result = matched.result
        self.resultHistogram = self.calcHistogram(self.result)

        height, width, channels = self.result.shape
        bytesPerLine = channels * width
        qImg = QImage(self.result.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

        self.resultLoaded = True
        pix = QPixmap(qImg)

        w = self.resultGroupBox.width()
        h = self.resultGroupBox.height() / 2

        self.resultHistogram = self.calcHistogram(self.result)
        canvas = PlotCanvas(self.resultHistogram, height=h/100, width=w/100)

        label = QLabel('Result image')
        label.setPixmap(pix.scaled(w, h, Qt.KeepAspectRatio))
        label.setAlignment(Qt.AlignCenter)
        self.resultGroupBox.layout().addWidget(label)
        self.resultGroupBox.layout().addWidget(canvas)

    def calcHistogram(self, I):
        # Calculate histogram
        b, g, r = cv2.split(I)

        rHistogram = np.zeros((256), dtype=int)
        gHistogram = np.zeros((256), dtype=int)
        bHistogram = np.zeros((256), dtype=int)

        for h in range(b.shape[0]):
            for w in range(b.shape[1]):
                rHistogram[r[h][w]] += 1
                gHistogram[g[h][w]] += 1
                bHistogram[b[h][w]] += 1

        histogram = np.zeros((3, 256), dtype=int)
        histogram[0] = rHistogram
        histogram[1] = gHistogram
        histogram[2] = bHistogram

        return histogram

    def deleteItemsFromWidget(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    deleteItemsFromWidget(item.layout())

class HistogramMatcher:
    def __init__(self, i, iHist, t, tHist):
        iHeight, iWidth, _ = i.shape 
        self.iSize = iHeight * iWidth

        tHeight, tWidth, _ = t.shape 
        self.tSize = tHeight * tWidth

        self.constructLUT(iHist, tHist)
        self.arrangeResult(i)

    def calculateCDF(self, hist, size):
        length = len(hist[0])
        pdf = np.zeros((3,length))
        pdf[:] = hist[:] / size

        cdf = np.zeros((3,length))

        for c in range(3):
            cdf[c] = np.cumsum(pdf[c])

        return cdf

    def constructLUT(self, iHist, tHist):
        cdfI = self.calculateCDF(iHist, self.iSize)
        cdfT = self.calculateCDF(tHist, self.tSize)

        self.lut = np.zeros((3, 256), dtype=int)

        for c in range(3):
            g_j = 0
            for g_i in range(256):
                while cdfT[c][g_j] < cdfI[c][g_i] and g_j < 255:
                    g_j += 1
                self.lut[c][g_i] = g_j

    def arrangeResult(self, i):
        self.result = i

        self.result[:,:,0] = self.lut[2][i[:,:,0]]
        self.result[:,:,1] = self.lut[1][i[:,:,1]]
        self.result[:,:,2] = self.lut[0][i[:,:,2]]

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        self.f = plt.figure(figsize=(height, width))
        FigureCanvas.__init__(self, self.f)

        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        self.f.add_subplot(3, 1, 1)
        plt.bar(range(256), hist[0], align='center', alpha=0.5, color='r')
        self.f.add_subplot(3, 1, 2)
        plt.bar(range(256), hist[1], align='center', alpha=0.5, color='g')
        self.f.add_subplot(3,1,3)
        plt.bar(range(256), hist[2], align='center', alpha=0.5, color='b')

        plt.tight_layout()

        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())