#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 16:56:30 2017

@author: aure
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMenu, QMainWindow, QAction, qApp, QApplication, QFileDialog,  QInputDialog, QLineEdit, QTableWidget, QTableWidgetItem, QTabWidget, QApplication, QComboBox, QFormLayout, QGroupBox, QColorDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon

import main

class Graphiques_main(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = "Application"
        self.InitUi()   

    def InitUi(self):  
        self.barre_statut = self.statusBar()
        self.barre_statut.showMessage('Bienvenue les couards !')
        
        self.menu_bar = self.menuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.addMenu("file")
        
        
        
        
        
        central_widget = QWidget()
        wind = QVBoxLayout()
        
        self.Graphiques = main.Graphiques(parent=self)
        
        wind.addWidget(self.Graphiques)
        central_widget.setLayout(wind)
        
        
        self.setCentralWidget(central_widget)
        self.show()
        


        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Graphiques_main()
    sys.exit(app.exec_())  