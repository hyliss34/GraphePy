#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:31:45 2017

@author: aure
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QTabWidget, QApplication, QComboBox, QFormLayout, QGroupBox, QColorDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileSystemModel, QTreeView




from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


import numpy as np
import pandas as pd


# Fenetre de choix du fichier
class dialog_fichier(QtWidgets.QDialog):
    
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
        ouvrir.setAutoDefault(True)
        
        # Bouton annuler
        annuler = QtWidgets.QPushButton("annuler")
        annuler.clicked.connect(self.reject)
        annuler.setAutoDefault(False)
        
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

        
 # ------------------- Tab 1 (Graphique) -----------------------------       
class Tab1(QWidget):
    def __init__(self,parent):
        super().__init__()
        # variable pour le data du fichier
        parent.data =[]
        #BOuton test
        parent.test = QPushButton("test")
        parent.test.clicked.connect(parent.test_func)
        
        # Formulaire
        parent.formGroupBox = QGroupBox("Paramètres")
        layout = QFormLayout()
        
        parent.choose_file = QtWidgets.QPushButton("Choisir le fichier csv")
        parent.choose_file.clicked.connect(parent.ouvre_arborescence)
        parent.path = ''
        
        
        parent.colx = QComboBox()
        parent.coly = QComboBox()
        
        parent.tracer = QtWidgets.QPushButton("Tracer")
        parent.tracer.clicked.connect(parent.Trace)
        
        # Choux couleur
        parent.color_btn = QtWidgets.QPushButton("Choisir couleur")
        parent.color_btn.clicked.connect(parent.fig_color)
        parent.color = 'b'
        
        # Choix marqueur
        marqueurs = Line2D.markers.keys()
        parent.marqueur = '.'
        parent.mark = QComboBox()
        for i in marqueurs:
            parent.mark.addItem(str(i))
            
        parent.mark.currentIndexChanged.connect(parent.fig_marqueur)
        
        # linestyles
        parent.current_linestyle = '-'
        linestyles = ['-', '--', '-.', ':','steps','None']
        parent.linestyle = QComboBox()
        for i in linestyles:
            parent.linestyle.addItem(str(i))
        parent.linestyle.currentIndexChanged.connect(parent.fig_linestyle)
        
        # Tracer
        parent.fig = Figure()
        parent.sub1 = parent.fig.add_subplot(111)
        parent.sub1.plot([],[],'r')
        
        
        
        
        parent.canvas = FigureCanvas(parent.fig)
        parent.tab1.layout.addWidget(parent.canvas)
        
        layout.addRow(parent.test)
        layout.addRow(parent.choose_file)
        layout.addRow(QtWidgets.QLabel("x: "), parent.colx)
        layout.addRow(QtWidgets.QLabel("y: "), parent.coly)
        layout.addRow(parent.tracer)
        layout.addRow(parent.color_btn)
        layout.addRow(QtWidgets.QLabel('Marqueur:'), parent.mark)
        layout.addRow(QtWidgets.QLabel('line:'), parent.linestyle)
        parent.formGroupBox.setLayout(layout)
        parent.tab1.layout.addWidget(parent.formGroupBox)
        
# ---------------------------------------------------------------------------
class Tab2(QWidget):
    
    def __init__(self, parent):
        super().__init__()        
        
        
        self.tableau = QTableWidget()
        
        
        self.txt = QtWidgets.QLabel('')
        parent.tab2.layout.addWidget(self.tableau)
        
        
        
        
        
        
# ---------------------------------------------------------------------------       
class Graphiques(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphique")
        self.initUI()
        self.show()
      
    def initUI(self):
        
        self.layout = QVBoxLayout()
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")

        
        self.tab1.layout = QHBoxLayout()
        self.tab2.layout = QVBoxLayout()
        
# ------------------- Tab 1 (Graphique) -----------------------------        
        self.TAB1 = Tab1(self)
# -------------------- Tab 2 (données) ------------------------------
        self.TAB2 = Tab2(self)
# -------------------------------------------------------------------   
    
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        

        
        
    # Fonction test   
    def test_func(self):
        m = np.linspace(0,10,10)

        
    # Ouvre fenetre de dialogue pour choisir le fichier (class Dialog)
    def ouvre_arborescence(self):
        Dialog = dialog_fichier(self)
        Dialog.show()
        
        
        
    # recupere les données et remplis les listes déroulantes (x et y)
    def parse_file(self):
        self.data = pd.read_csv(self.path, delimiter=",")
        headers = self.data.columns.values.tolist()
        
        nl = self.data.shape[0]
        ncol = self.data.shape[1]
        self.TAB2.tableau.setColumnCount(ncol)
        self.TAB2.tableau.setRowCount(nl)
        self.TAB2.tableau.setHorizontalHeaderLabels(headers)
        for i in range(nl):
            for j in range(ncol):
                self.TAB2.tableau.setItem(i,j,QTableWidgetItem(str(self.data.iloc[i][j])))

        
        print(self.data)
        
        
        print(headers)
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
            
            self.replot_fig()
      
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