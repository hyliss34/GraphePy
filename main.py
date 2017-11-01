#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:31:45 2017

@author: aure
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit, QTableWidget, QTableWidgetItem, QTabWidget, QApplication, QComboBox, QFormLayout, QGroupBox, QColorDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileSystemModel, QTreeView




from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


import numpy as np
import pandas as pd


# Fenetre de choix du fichier
class dialog_fichier(QtWidgets.QDialog):
    
    def __init__(self,Main,parent):
        QtWidgets.QDialog.__init__(self,Main)
        self.main = Main
        self.parent = parent
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
        print("d")
        index = self.tree.currentIndex()
        print("d")
        self.main.path = self.model.filePath(index) # recupere le path du fichier cliqué
        print("d")
        self.reject() # ferme la fenetre de dialogue
        print("d")
        self.main.parse_file() # lance le parse pour remplir les listes x et y

        
 # ------------------- Tab 1 (Graphique) -----------------------------       
class Tab1(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
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
        
        #Size line
        self.current_linewidth = 2
        self.linewidth = QtWidgets.QLineEdit()
        self.valide_linewidth = QtWidgets.QPushButton("ok")
        self.valide_linewidth.clicked.connect(self.fig_linewidth)
        hb_mini = QHBoxLayout()
        hb_mini.addWidget(self.linewidth)
        hb_mini.addWidget(self.valide_linewidth)
        
        
        # Labels
        self.xlabel = ''
        self.ylabel = ''
        self.widg_xlabel = QtWidgets.QLineEdit()
        self.widg_ylabel = QtWidgets.QLineEdit()
        
        
        # Tracer
        self.fig = Figure()
        self.sub1 = self.fig.add_subplot(111)
        self.sub1.plot([],[],'r')
        
        self.canvas = FigureCanvas(self.fig)
        parent.tab1.layout.addWidget(self.canvas)
        
        # Formulaire
        layout.addRow(self.test)
        layout.addRow(self.choose_file)
        layout.addRow(QtWidgets.QLabel("x "), self.colx)
        layout.addRow(QtWidgets.QLabel("y "), self.coly)
        layout.addRow(QtWidgets.QLabel("Label x"), self.widg_xlabel)
        layout.addRow(QtWidgets.QLabel("Label y"), self.widg_ylabel)
        layout.addRow(self.tracer)
        layout.addRow(self.color_btn)
        layout.addRow(QtWidgets.QLabel('Marqueur '), self.mark)
        layout.addRow(QtWidgets.QLabel('Style '), self.linestyle)
        layout.addRow(QtWidgets.QLabel('Epaisseur '), hb_mini)
        self.formGroupBox.setLayout(layout)
        parent.tab1.layout.addWidget(self.formGroupBox)
        
        # Fonction test   
    def test_func(self):
        m = np.linspace(0,10,10)

        
    # Ouvre fenetre de dialogue pour choisir le fichier (class Dialog)
    def ouvre_arborescence(self):
        Dialog = dialog_fichier(self,self.parent)
        Dialog.show()
    
    # Efface et Retrace le figure 
    def replot_fig(self):
        self.fig.clf() 
        self.sub1 = self.fig.add_subplot(111)
        
        # Labels
        if self.widg_xlabel.text() != '':
            self.xlabel = self.widg_xlabel.text()
        else:
            self.xlabel = self.colx.currentText()
        if self.widg_ylabel.text() != '':
            self.ylabel = self.widg_ylabel.text()
        else:
            self.ylabel = self.coly.currentText()
        
        self.sub1.set_xlabel(self.xlabel)
        self.sub1.set_ylabel(self.ylabel)
        self.sub1.plot(self.data_x, self.data_y, linestyle=self.current_linestyle,  marker = self.marqueur, color=self.color, linewidth = self.current_linewidth)
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
        
    def fig_linewidth(self):
        self.current_linewidth = float(self.linewidth.text())
        
        self.replot_fig()
        
    # Utilise les données et la selection x et y pour tracer le graphique
    def Trace(self):
        if(self.colx == 0 or self.coly==0):
            print("Erreur : Pas de données")
        else:
            self.data_x = self.data[str(self.colx.currentText())]
            self.data_y = self.data[str(self.coly.currentText())]
            
            self.replot_fig()
            
       # recupere les données et remplis les listes déroulantes (x et y)
    def parse_file(self):
        
        self.data = pd.read_csv(self.path, delimiter=",")
        headers = self.data.columns.values.tolist()
        
        nl = self.data.shape[0]
        ncol = self.data.shape[1]
        self.parent.TAB2.tableau.setColumnCount(ncol)
        self.parent.TAB2.tableau.setRowCount(nl)
        self.parent.TAB2.tableau.setHorizontalHeaderLabels(headers)
        for i in range(nl):
            for j in range(ncol):
                self.parent.TAB2.tableau.setItem(i,j,QTableWidgetItem(str(self.data.iloc[i][j])))

        for i in headers:
            self.colx.addItem(i)
            self.coly.addItem(i)
        
# ---------------------------------------------------------------------------
class Tab2(QWidget):
    
    def __init__(self, parent):
        super().__init__()        
        self.tableau = QTableWidget()
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
        self.tabs.addTab(self.tab1,"Graphique")
        self.tabs.addTab(self.tab2,"Données")

        
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
        

        
        

        
        
        
 


      
    


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Graphiques()
    sys.exit(app.exec_())        