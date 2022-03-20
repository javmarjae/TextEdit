import os
from .base import Controller

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog
from utils.i18n import trans


class FileController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.filePath = ''

    #Función abrir documento de texto
    def fileOpen(self):
        #Establecemos el archivo que queremos abrir 
        file,_ = QFileDialog.getOpenFileName(self.app, trans('Open file'))

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Guardamos la ruta
        self.filePath = file

        name = os.path.basename(self.filePath)
        self.app.setWindowTitle('%s | TextEdit' %name)

        #Establecemos la lectura en HTML en paralelo
        self.app.views.openSubWindow()  

        #Abrimos el archivo y lo mandamos a la funcion para escribir
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        self.writeFile(file, text)
        
    #Función nuevo archivo
    def fileNew(self):
        #Establecemos el lugar en el que vamos a guardar el archivo
        file,_ = QFileDialog.getSaveFileName(self.app, trans('New file'))

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Guardamos la ruta
        self.filePath = file

        name = os.path.basename(self.filePath)
        self.app.setWindowTitle('%s | TextEdit' %name)

        #Establecemos la lectura en HTML en paralelo
        self.app.views.openSubWindow()      

        #Abrimos el archivo en la función para escribir
        self.writeFile(file, text = '')
        
    #Función para escribir en un archivo
    def writeFile(self,file,text):
        #Activo la edición
        self.app.textEdit.setReadOnly(False)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
            self.app.textEdit.setText(text)
            
    #Función para guardar los cambios
    def fileSaveChanges(self):  

        if not self.filePath:
            return

        #Definimos la función de guardado de un archivo
        with open(self.filePath, 'w', encoding='utf-8') as f:
            text = self.app.textEdit.toPlainText()
            f.write(text)
    
    def saveAs(self):
        file,_ = QFileDialog.getSaveFileName(self.app, trans('New file'))

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Definimos la función de guardado de un archivo
        with open(file, 'w', encoding='utf-8') as f:
            text = self.app.textEdit.toPlainText()
            f.write(text)