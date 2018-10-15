#!/usr/local/bin/python3

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication

class HistogramApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):         
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        inputAct = QAction('Open input', self)
        targetAct = QAction('Open target', self) 

        exitAct = QAction('Exit', self)        
        exitAct.triggered.connect(qApp.quit)

        fileMenu.addAction(inputAct)
        fileMenu.addAction(targetAct)
        fileMenu.addAction(exitAct)
        
        self.setGeometry(250, 200, 750, 400)
        self.setWindowTitle('Histogram Matching')    
        self.show()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    histogramApp = HistogramApp()
    sys.exit(app.exec_())