#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:31:45 2017

@author: aure
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog,  QInputDialog, QLineEdit, QTableWidget, QTableWidgetItem, QTabWidget, QApplication, QComboBox, QFormLayout, QGroupBox, QColorDialog, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileSystemModel, QTreeView




from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


import numpy as np
import pandas as pd


####################################################################################################################################################
###   Fenetre de fichiers
#####################################################################################################################################################
class App(QWidget):
 
    def __init__(self,Main):
        super().__init__()
        self.main = Main
        self.title = 'PyQt5 file dialogs'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        #self.openFileNameDialog()
        #self.openFileNamesDialog()
        #self.saveFileDialog()

 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName
            
 
    def openFileNamesDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
    
    
    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            return fileName
        
####################################################################################################################################################
###   Tab 1
#####################################################################################################################################################     
class Tab1(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.data =[]

        #Bouton test
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
        
        # Titre
        self.titre = QtWidgets.QLineEdit()
        
        self.hb_mini2 = QHBoxLayout()
        # ticks
        self.ticks_state = 'on'
        self.ticks = QtWidgets.QCheckBox()
        self.ticks.setCheckState(2)
        self.ticks.stateChanged.connect(self.ticks_or_not)
        
        # Spines (arretes)
        self.spine_state = True
        self.spine = QtWidgets.QCheckBox()
        self.spine.setCheckState(2)
        self.spine.stateChanged.connect(self.spine_or_not)
        
        self.hb_mini2.addWidget(QtWidgets.QLabel('Ticks '))
        self.hb_mini2.addWidget(self.ticks)
        self.hb_mini2.addWidget(QtWidgets.QLabel('Arretes '))
        self.hb_mini2.addWidget(self.spine)
        
        # Tracer
        self.fig = Figure()
        
        
        self.canvas = FigureCanvas(self.fig)
        parent.tab1.layout.addWidget(self.canvas)
        
        # Sauvegarde
        self.sauvegarde = QtWidgets.QPushButton("Save")
        self.sauvegarde.clicked.connect(self.save_fig)
        
        
        
        # Formulaire
        layout.addRow(self.test)
        layout.addRow(self.choose_file)
        layout.addRow(QtWidgets.QLabel("x "), self.colx)
        layout.addRow(QtWidgets.QLabel("y "), self.coly)
        layout.addRow(QtWidgets.QLabel("Label x"), self.widg_xlabel)
        layout.addRow(QtWidgets.QLabel("Label y"), self.widg_ylabel)
        layout.addRow(QtWidgets.QLabel("Titre"), self.titre)        
        layout.addRow(self.tracer)
        layout.addRow(self.color_btn)
        layout.addRow(QtWidgets.QLabel('Marqueur '), self.mark)
        layout.addRow(QtWidgets.QLabel('Style '), self.linestyle)
        layout.addRow(QtWidgets.QLabel('Epaisseur '), hb_mini)
        layout.addRow(self.hb_mini2)
        layout.addRow(self.sauvegarde)
        self.formGroupBox.setLayout(layout)
        parent.tab1.layout.addWidget(self.formGroupBox)
        

    def test_func(self):
        print("ok")
        print(self.ticks.isChecked())
     
       
    #########################################################
    ###   Sauvegarde
    #########################################################
    def save_fig(self):
        try:
            file = App(self).saveFileDialog()
            file.show()
        finally:
            self.fig.savefig(file)

        
    #########################################################
    ###   Ouvrir fichier 
    #########################################################
    def ouvre_arborescence(self):
        try:
            open_fichier = App(self).openFileNameDialog()
            open_fichier.show()
        finally:
            self.path = open_fichier
            self.parse_file()
    
    #########################################################
    ###   Replot
    #########################################################
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
        
        # Ticks
        self.sub1.tick_params(bottom=self.ticks_state, left=self.ticks_state)
        
        # Titre
        self.sub1.set_title(self.titre.text())
        
        # Spines (ligne de contour)
        for key,spine in self.sub1.spines.items():
            spine.set_visible(self.spine_state)
        
        
        self.sub1.plot(self.data_x, self.data_y, linestyle=self.current_linestyle,  marker = self.marqueur, color=self.color, linewidth = self.current_linewidth)
        self.canvas.draw()

    #########################################################
    ###   Boutons figure live update (marqueurs, linestyle, linewidth, ticks, arretes
    #########################################################
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
        
    def ticks_or_not(self):
        if(self.ticks.isChecked()):
            self.ticks_state = "on"
            self.replot_fig()
        else:
            self.ticks_state = "off"
            self.replot_fig() 
            
    def spine_or_not(self):
        if(self.spine.isChecked()):
            self.spine_state = True
            self.replot_fig()
        else:
            self.spine_state = False
            self.replot_fig()
    
        
    #########################################################
    ###   Bouton tracer
    #########################################################
    def Trace(self):
        if(self.colx == 0 or self.coly==0):
            print("Erreur : Pas de données")
        else:
            self.data_x = self.data[str(self.colx.currentText())]
            self.data_y = self.data[str(self.coly.currentText())]
            
            self.replot_fig()
            
    #########################################################
    ###   Recuperation des données du fichier
    #########################################################
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
        
####################################################################################################################################################
###   Tab 2
#####################################################################################################################################################
class Tab2(QWidget):
    
    def __init__(self, parent):
        super().__init__()        
        self.tableau = QTableWidget()
        parent.tab2.layout.addWidget(self.tableau)
        
        
        
        
        
        
####################################################################################################################################################
###   Appli principale
#####################################################################################################################################################      
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
        self.tab3 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1,"Graphique")
        self.tabs.addTab(self.tab2,"Données")
        self.tabs.addTab(self.tab3,"Vide")
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