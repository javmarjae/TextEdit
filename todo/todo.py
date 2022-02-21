
from msilib.schema import Shortcut
import sys
import json
import os
from xml.dom.minidom import Document

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QTextCursor 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)
tick = QtGui.QImage('tick.png')


class TodoModel(QtCore.QAbstractListModel):
    #Este es el todoModel que venia con el esqueleto del programa
    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos = todos or [] 
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, text = self.todos[index.row()]
            return text
        
        if role == Qt.DecorationRole:
            status, _ = self.todos[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.todos)


class MainWindow(QMainWindow, Ui_MainWindow):

    #Inicializamos
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = TodoModel()
        self.load()
        self.lineEdit = QLineEdit()
        self.textEdit = QTextEdit()
        self.clipboard = QApplication.clipboard()
        self.statusBar = QStatusBar()
        self.cursor = QtGui.QTextCursor()
        self.setFocus()
        self._createActions()
        self._createMenuBar()
        self._createToolBars()
        
        
    #Creamos la barra de menu
    def _createMenuBar(self):
        menuBar = QMenuBar(self)

        #Añadimos los tres menus: archivo, editar y ayuda
        fileMenu = QMenu("&Archivo", self)
        editMenu = QMenu("&Editar", self)
        helpMenu = QMenu("&Ayuda", self)

        #Añadimos el menu archivo con sus acciones
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newFile)
        fileMenu.addAction(self.openFile)
        fileMenu.addAction(self.saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(self.closeApp)

        #Añadimos el menu editar con sus acciones
        menuBar.addMenu(editMenu)
        editMenu.addAction(self.copyText)
        editMenu.addAction(self.pasteText)
        editMenu.addAction(self.cutText)
        editMenu.addSeparator()
        editMenu.addAction(self.undo)
        editMenu.addAction(self.redo)

        #Añadimos el menu ayuda con sus acciones
        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.help)
        helpMenu.addSeparator()
        helpMenu.addAction(self.about)

        self.setMenuBar(menuBar)

    #Creamos la barra de herramientas
    def _createToolBars(self):
        fileToolBar = QToolBar('Archivo',self)
        editToolBar = QToolBar('Archivo',self)

        self.addToolBar(fileToolBar)
        self.addToolBar(editToolBar)

        fileToolBar.addAction(self.newFile)
        fileToolBar.addAction(self.openFile)
        fileToolBar.addAction(self.saveFile)

        fileToolBar.setMovable(False)

        editToolBar.addAction(self.copyText)
        editToolBar.addAction(self.pasteText)
        editToolBar.addAction(self.cutText)
        editToolBar.addSeparator()
        self.fontSizeBox = QSpinBox()
        self.fontSizeBox.setFocusPolicy(Qt.NoFocus)
        editToolBar.addWidget(self.fontSizeBox)
        editToolBar.addAction(self.bold)
        editToolBar.addAction(self.striketrhough)
        editToolBar.addAction(self.underline)
        editToolBar.addSeparator()
        editToolBar.addAction(self.header1)
        editToolBar.addAction(self.header2)
        editToolBar.addAction(self.header3)
        editToolBar.addSeparator()
        editToolBar.addAction(self.undo)
        editToolBar.addAction(self.redo)

        editToolBar.setMovable(False)
       


    #Creamos las acciones que se añaden a los menus
    def _createActions(self):

        self.newFile = QAction(QIcon("resources/newFile.png"),'Nuevo', self, triggered = self.fileNew, shortcut = 'Ctrl+n')
        self.newFile.setStatusTip('Nuevo archivo')

        self.openFile = QAction(QIcon("resources/openFile.png"),'Abrir', self, triggered = self.fileOpen, shortcut = 'Ctrl+a')
        self.openFile.setStatusTip('Abrir archivo')

        self.saveFile = QAction(QIcon("resources/saveFile.png"),'&Guardar', self, triggered = self.fileSave, shortcut = 'Ctrl+s')
        self.saveFile.setStatusTip('Guardar cambios')

        self.closeApp = QAction('Cerrar', self, triggered = self.close, shortcut = 'Ctrl+q')
        self.closeApp.setStatusTip('Cerrar aplicacion')

        self.copyText = QAction(QIcon("resources/copy.png"),'Copiar', self, triggered = self.textCopy, shortcut = 'Ctrl+c')
        self.copyText.setStatusTip('Copiar el texto seleccionado')

        self.pasteText = QAction(QIcon("resources/paste.png"),'Pegar', self, triggered = self.textPaste, shortcut = 'Ctrl+v')
        self.pasteText.setStatusTip('Pegar del portapapeles')

        self.cutText = QAction(QIcon("resources/cut.png"),'Cortar', self, triggered = self.textCut, shortcut = 'Ctrl+x')
        self.cutText.setStatusTip('Cortar el texto seleccionado')

        self.undo = QAction(QIcon("resources/undo.png"), 'Deshacer', self, shortcut = 'Ctrl+z')
        self.undo.setStatusTip('Deshacer')
        #self.undo.triggered.connect(QUndoCommand.undo())

        self.redo = QAction(QIcon("resources/redo.png"), 'Rehacer', self, shortcut = 'Ctrl+y')
        self.redo.setStatusTip('Rehacer')
        #self.redo.triggered.connect(QUndoCommand.redo())

        self.header1 = QAction(QIcon("resources/header1.png"), 'Título 1', self)
        self.header1.setShortcut('Ctrl+h+1')
        self.header1.setStatusTip('Título 1')

        self.header2 = QAction(QIcon("resources/header2.png"), 'Título 2', self)
        self.header2.setShortcut('Ctrl+h+2')
        self.header2.setStatusTip('Título 2')

        self.header3 = QAction(QIcon("resources/header3.png"), 'Título 3', self)
        self.header3.setShortcut('Ctrl+h+3')
        self.header3.setStatusTip('Título 3')

        self.bold = QAction(QIcon("resources/bold.png"), 'Negrita', self)
        self.bold.setShortcut('Ctrl+n')
        self.bold.setStatusTip('Texto marcado')

        self.underline = QAction(QIcon("resources/underline.png"), 'Subrayado', self)
        self.underline.setShortcut('Ctrl+u')
        self.underline.setStatusTip('Texto subrayado')

        self.striketrhough = QAction(QIcon("resources/striketrhough.png"), 'Cursiva', self)
        self.striketrhough.setShortcut('Ctrl+k')
        self.striketrhough.setStatusTip('Texto en cursiva')

        self.help = QAction('Ayuda', self)
        self.help.setShortcut('Ctrl+h')
        self.help.setStatusTip('Ayuda')

        self.about = QAction('Acerda de TextEdit', self)
        self.about.setStatusTip('Acerda de TextEdit')

    #Función cerrar que pregunta al usuario si está seguro antes de hacerlo
    def close(self):
        choice = QMessageBox.question(self, 'Salir', '¿Está seguro de que quiere cerrar TextEdit?', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Si:
            qApp.quit
        else: pass

    #Función abrir documento de texto
    def fileOpen(self):
        #Establecemos el archivo que queremos abrir 
        file,_ = QFileDialog.getOpenFileName(self, 'Abrir archivo')

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        fileOpen = open(file)

        #Guardamos la ruta
        self.filePath = file

        #Establecemos el widget para escritura
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        #Abrimos el archivo y guardamos en una variable todo el texto que contiene para mostrarlo
        with fileOpen:
            text = fileOpen.read()
            self.textEdit.setText(text) 

    def fileNew(self):
        #Establecemos el lugar en el que vamos a guardar el archivo
        file,_ = QFileDialog.getSaveFileName()

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Guardamos la ruta
        self.filePath = file

        #Establecemos el widget para escritura
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        #Abrimos el archivo con opción de escritura
        if file:
            with open(file,'w'):
                text = ''
                self.textEdit.setText(text)

    #Función para guardar los cambios
    def fileSave(self):

        #Obtengo la ruta del archivo abierto
        file = self.filePath

        #Definimos la función de guardado de un archivo
        with open(file, 'w') as file:
            text = self.textEdit.toPlainText()
            file.write(text)    

    #Función copiar
    def textCopy(self):
        tc = self.textEdit.textCursor()
        text = QTextCursor.selectedText(tc)
        self.clipboard.setText(text)

    #Función pegar
    def textPaste(self):
        tc = self.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            QTextCursor.removeSelectedText(tc)
        tc.insertText(self.clipboard.text())
    
    #Función cortar
    def textCut(self):
        tc = self.textEdit.textCursor()
        text = QTextCursor.selectedText(tc)
        self.clipboard.setText(text)
        QTextCursor.removeSelectedText(tc)

    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        if text: # Don't add empty strings.
            # Access the list via the model.
            self.model.todos.append((False, text))
            # Trigger refresh.        
            self.model.layoutChanged.emit()
            # Empty the input
            self.todoEdit.setText("")
            self.save()
        
    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()
            
    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal 
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            # Clear the selection (as it is no longer valid).
            self.todoView.clearSelection()
            self.save()
    
    def load(self):
        try:
            with open('data.db', 'r') as f:
                self.model.todos = json.load(f)
        except Exception:
            pass

    def save(self):
        with open('data.db', 'w') as f:
            data = json.dump(self.model.todos, f)


app = QApplication(sys.argv)
GUI = MainWindow()
GUI.show()
app.exec_()


