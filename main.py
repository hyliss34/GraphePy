#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:31:45 2017

@author: aure
"""
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QComboBox, QFormLayout, QGroupBox, QColorDialog, QWidget,QVBoxLayout,QGridLayout,QLabel,QHBoxLayout,QLineEdit,QPushButton, QFileSystemModel, QTreeView
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import animation
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class dialog(QtWidgets.QDialog):
    
    def __init__(self,Main):
        QtWidgets.QDialog.__init__(self,Main)
        self.main = Main
        self.setWindowTitle("Choix du fichier")
        
        # Boite de sialogue avec le systeme de fichier
        self.model = QFileSystemModel()
        self.model.setRootPath('/Users')
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.doubleClicked.connect(self.choix_fichier)
        
        # Bouton ouvrir
        ouvrir = QtWidgets.QPushButton("ouvrir")
        ouvrir.clicked.connect(self.choix_fichier)
        
        # Bouton annuler
        annuler = QtWidgets.QPushButton("annuler")
        annuler.clicked.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        hb1 = QHBoxLayout()
        hb1.addWidget(annuler)
        hb1.addWidget(ouvrir)
        layout.addLayout(hb1)
        self.setLayout(layout)
    
    def choix_fichier(self):
        index = self.tree.currentIndex()
        self.main.path = self.model.filePath(index) # recupere le path du fichier cliqué
        self.reject() # ferme la fenetre de dialogue
        self.main.parse_file() # lance le parse pour remplir les listes x et y
        
        
        
        
        
class Graphiques(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphique")
        self.initUI()
        self.show()
      
    def initUI(self):
        
        mainLayout = QHBoxLayout()
        # variable pour le data du fichier
        self.data =[]
        #BOuton test
        self.test = QPushButton("test")
        self.test.clicked.connect(self.test_func)
        
        # Formulaire
        self.formGroupBox = QGroupBox("Paramètres")
        layout = QFormLayout()
        
        self.choose_file = QtWidgets.QPushButton("Choisir le fichier csv")
        self.choose_file.clicked.connect(self.ouvre_arborescence)
        self.path = ''
        
        
        self.colx = QComboBox()
        self.coly = QComboBox()
        
        self.tracer = QtWidgets.QPushButton("Tracer")
        self.tracer.clicked.connect(self.Trace)
        
        # Choux couleur
        self.color_btn = QtWidgets.QPushButton("Choisir couleur")
        self.color_btn.clicked.connect(self.fig_color)
        self.color = 'b'
        
        # Choix marqueur
        marqueurs = Line2D.markers.keys()
        self.marqueur = '.'
        self.mark = QComboBox()
        for i in marqueurs:
            self.mark.addItem(str(i))
            
        self.mark.currentIndexChanged.connect(self.fig_marqueur)
        
        # linestyles
        self.current_linestyle = '-'
        linestyles = ['-', '--', '-.', ':','steps','None']
        self.linestyle = QComboBox()
        for i in linestyles:
            self.linestyle.addItem(str(i))
        self.linestyle.currentIndexChanged.connect(self.fig_linestyle)
        
        # tracer
        self.fig = Figure()
        self.sub1 = self.fig.add_subplot(111)
        self.sub1.plot([],[],'r')
        
        
        
        
        self.canvas = FigureCanvas(self.fig)
        mainLayout.addWidget(self.canvas)
        
        layout.addRow(self.test)
        layout.addRow(self.choose_file)
        layout.addRow(QtWidgets.QLabel("x: "), self.colx)
        layout.addRow(QtWidgets.QLabel("y: "), self.coly)
        layout.addRow(self.tracer)
        layout.addRow(self.color_btn)
        layout.addRow(QtWidgets.QLabel('Marqueur:'),self.mark)
        layout.addRow(QtWidgets.QLabel('line:'),self.linestyle)
        self.formGroupBox.setLayout(layout)
        mainLayout.addWidget(self.formGroupBox)
        
        
        self.setLayout(mainLayout)
        

        
        
    # Fonction test   
    def test_func(self):
        m = np.linspace(0,10,10)

        
    # Ouvre fenetre de dialogue pour choisir le fichier (class Dialog)
    def ouvre_arborescence(self):
        Dialog = dialog(self)
        Dialog.show()
        
    # recupere les données et remplis les listes déroulantes (x et y)
    def parse_file(self):
        self.data = pd.read_csv(self.path, delimiter=",")
        headers = self.data.columns.values.tolist()
        for i in headers:
            self.colx.addItem(i)
            self.coly.addItem(i)

    # Utilise les données et la selection x et y pour tracer le graphique
    def Trace(self):
        if(self.colx == 0 or self.coly==0):
            print("Erreur : Pas de données")
        else:
            self.data_x = self.data[str(self.colx.currentText())]
            self.data_y = self.data[str(self.coly.currentText())]
            
            self.sub1.plot(self.data_x, self.data_y, linestyle=self.current_linestyle, marker = self.marqueur, color=self.color)
            self.canvas.draw()
      
    # Efface et Retrace le figure 
    def replot_fig(self):
        self.fig.clf() 
        self.sub1 = self.fig.add_subplot(111)
        self.sub1.plot(self.data_x, self.data_y, linestyle=self.current_linestyle,  marker = self.marqueur, color=self.color)
        self.canvas.draw()
        
    def fig_color(self):
        color = QColorDialog.getColor()
        self.color = color.name()
        
        self.replot_fig()
     
    def fig_marqueur(self):
        self.marqueur = str(self.mark.currentText())
        
        self.replot_fig()

    def fig_linestyle(self):
        self.current_linestyle = str(self.linestyle.currentText())
        
        self.replot_fig()


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Graphiques()
    sys.exit(app.exec_())        