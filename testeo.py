#!/usr/bin/env python

from fileinput import close, filename
import imp
import sys
import os

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *


class App(QMainWindow):

    def __init__(self,parent=None):

        QWidget.__init__(self, parent)

        #Se define el tamano de la ventana
        self.setGeometry(0, 50, 600, 400)

        #Se le coloca un titulo a la ventana y se asocia un icono.
        self.setWindowTitle('Editor de Texto:')
        self.setWindowIcon(QtGui.QIcon('./openlogo-50.png'))

        #Se define el widget de edicion de texto
        self.textEdit = QTextEdit()

        #Se coloca en el centro
        self.setCentralWidget(self.textEdit)

        #Se define la barra de estatus y se le asigna foco
        self.statusBar()
        self.setFocus()

        #Se define la accion abrir archivo, con evento de teclado y mensaje
        openFile = QAction('Abrir', self)
        openFile.setShortcut('Ctrl+a')
        openFile.setStatusTip('Abrir archivo nuevo')
        openFile.triggered.connect(self.showDialog)

        #Se define la accion cerrar aplicacion con evento de teclado y mensaje
        closeApp = QAction('Cerrar',self)
        closeApp.setShortcut('Ctrl+q')
        closeApp.setStatusTip('Cerrar aplicacion')
        closeApp.triggered.connect(qApp.quit)

        #Se define la acción de guardar archivo
        saveFile = QAction('Guardar', self)
        saveFile.setShortcut('Ctrl+s')
        saveFile.setStatusTip('Guardar cambios')
        saveFile.triggered.connect(self.fileSave)

        #Se define la barra de menu
        menubar = self.menuBar()

        #Nombre archivo y se agrega abrir y cerrar aplicacion a la barra de menús, con los nombres
        #previamente dichos y las acciones seteadas
        fileMenu = menubar.addMenu('&Archivo')

        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(closeApp)

    def fileSave(self):

        #Obtengo la ruta del archivo abierto
        file = self.filePath

        #Definimos la función de guardado de un archivo
        with open(file, 'w') as file:
            text = self.textEdit.toPlainText()
            file.write(text)

    def showDialog(self):

        #Se captura el nombre del archivo a abrir
        file,_ = QFileDialog.getOpenFileName(self, 'Abrir archivo', QtCore.QDir.homePath(), "All Files (*);;Text Files (*.txt)")

        #Defino la ruta del archivo abierto para poder usarla en otras funcionas
        self.filePath = file

        #Se cambia el título de la ventana
        filename = os.path.basename(file)
        self.setWindowTitle('Editor de Texto: %s' %filename)

        #Se abre el archivo y se despliega la informacion en el widget de edición de texto
        fname = open(file)
        data = fname.read()
        self.textEdit.setText(data)        

#Se ejecuta el programa principal

if __name__ == "__main__":    

   #Se instancia la clase QApplication    
   app = QApplication(sys.argv)    

   #Se instancia el objeto QuitButton    
   qb = App()    

   #Se muestra la aplicacion    
   qb.show()    

   #Se sale de la aplicacion    
   sys.exit(app.exec_())