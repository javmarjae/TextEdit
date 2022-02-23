import os
from .base import Controller

from PyQt5.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QFileDialog
from utils.i18n import trans


class FileController(Controller):
    #Función abrir documento de texto
    def fileOpen(self) -> None:
        #Establecemos el archivo que queremos abrir 
        file,_ = QFileDialog.getOpenFileName(self.app, trans('Open file'))

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Guardamos la ruta
        self.filePath = file

        name = os.path.basename(self.filePath)
        self.app.setWindowTitle('%s | TextEdit' %name)

        #Establecemos el widget para escritura y lectura en HTML en paralelo
        central_widget = QWidget()
        self.app.setCentralWidget(central_widget)

        self.app.views.openSubWindow()

        lay = QHBoxLayout(central_widget)
        lay.addWidget(self.app.textEdit,5)
        lay.addWidget(self.app.textPreview,5)

        #Abrimos el archivo y lo mandamos a la funcion para escribir
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        self.writeFile(file, text)

    def fileNew(self) -> None:
        #Establecemos el lugar en el que vamos a guardar el archivo
        file,_ = QFileDialog.getSaveFileName(self.app, trans('New file'))

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Guardamos la ruta
        self.filePath = file

        name = os.path.basename(self.filePath)
        self.app.setWindowTitle('%s | TextEdit' %name)

        #Establecemos el widget para escritura y lectura en HTML en paralelo
        central_widget = QWidget()
        self.app.setCentralWidget(central_widget)

        self.app.views.openSubWindow()

        lay = QHBoxLayout(central_widget)
        lay.addWidget(self.app.textEdit,5)
        lay.addWidget(self.app.textPreview,5)

        #Abrimos el archivo en la función para escribir
        self.writeFile(file, text = '')

    #Función para escribir en un archivo
    def writeFile(self,file,text) -> None:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
            self.app.textEdit.setText(text)
            

    #Función para guardar los cambios
    def fileSave(self) -> None:  

        if not self.filePath:
            return

        #Obtengo la ruta del archivo abierto
        file = self.filePath

        #Definimos la función de guardado de un archivo
        with open(file, 'w', encoding='utf-8') as file:
            text = self.app.textEdit.toPlainText()
            file.write(text)