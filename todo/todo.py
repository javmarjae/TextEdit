import logging
from posixpath import expanduser, normpath
import sys
import json
import os
import locale
import urllib.request
from xml.dom.minidom import Document

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QTextCursor 
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import Qt, pyqtProperty, pyqtSignal, QObject, QTextCodec, QUrl
from markdown import markdown
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtWebChannel import QWebChannel
from i18n import trans


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class Document(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_text = ''

    def get_text(self):
        return self.m_text

    def set_text(self, text):
        if self.m_text == text:
            return
        self.m_text = text
        self.textChanged.emit(self.m_text)

    textChanged = pyqtSignal(str)
    text = pyqtProperty(str, fget=get_text, fset=set_text, notify=textChanged)

class PreviewPage(QWebEnginePage):
    pass

class MainWindow(QMainWindow, Ui_MainWindow):

    #Inicializamos
    def __init__(self):
        super(QMainWindow,self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.lineEdit = QLineEdit()
        self.textPreview = QWebEngineView()
        self.textPreview.setContextMenuPolicy(Qt.NoContextMenu)
        self.textEdit = QTextEdit()
        self.clipboard = QApplication.clipboard()
        self.statusBar = QStatusBar()
        self.cursor = QtGui.QTextCursor()
        self.undoStack = QUndoStack()
        self.undoCommand = QUndoCommand()
        self.setFocus()
        self._createActions()
        self._createMenuBar()
        self._createToolBars()

    #Creamos la barra de menu
    def _createMenuBar(self):
        menuBar = QMenuBar(self)

        #Añadimos los tres menus: archivo, editar y ayuda
        fileMenu = QMenu("&File", self)
        editMenu = QMenu("&Edit", self)
        helpMenu = QMenu("&Help", self)

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
        fileToolBar = QToolBar('File',self)
        editToolBar = QToolBar('Edit',self)

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
        editToolBar.addAction(self.italic)
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

        self.newFile = QAction(QIcon("resources/icons/newFile.png"),'New', self, triggered = self.fileNew, shortcut = 'Ctrl+n')
        self.newFile.setStatusTip('New file')

        self.openFile = QAction(QIcon("resources/icons/openFile.png"),'Open', self, triggered = self.fileOpen, shortcut = 'Ctrl+a')
        self.openFile.setStatusTip('Open file')

        self.saveFile = QAction(QIcon("resources/icons/saveFile.png"),'Save', self, triggered = self.fileSave, shortcut = 'Ctrl+s')
        self.saveFile.setStatusTip('Save changes')

        self.closeApp = QAction('Close', self, triggered = self.close, shortcut = 'Ctrl+q')
        self.closeApp.setStatusTip('Close app')

        self.copyText = QAction(QIcon("resources/icons/copy.png"),'Copy', self, triggered = self.textCopy, shortcut = 'Ctrl+c')
        self.copyText.setStatusTip('Copy selected text')

        self.pasteText = QAction(QIcon("resources/icons/paste.png"),'Paste', self, triggered = self.textPaste, shortcut = 'Ctrl+v')
        self.pasteText.setStatusTip('Paste from clipboard')

        self.cutText = QAction(QIcon("resources/icons/cut.png"),'Cut', self, triggered = self.textCut, shortcut = 'Ctrl+x')
        self.cutText.setStatusTip('Cut selected text')

        self.undo = QAction(QIcon("resources/icons/undo.png"), 'Undo', self, shortcut = 'Ctrl+z')
        self.undo.setStatusTip('Undo')
        #self.undo.triggered.connect(QUndoCommand.undo())

        self.redo = QAction(QIcon("resources/icons/redo.png"), 'Redo', self, shortcut = 'Ctrl+y')
        self.redo.setStatusTip('Redo')
        #self.redo.triggered.connect(QUndoCommand.redo())

        self.header1 = QAction(QIcon("resources/icons/header1.png"), 'Header 1', self, triggered = self.textH1, shortcut='Ctrl+h+1')
        self.header1.setStatusTip('Header 1')

        self.header2 = QAction(QIcon("resources/icons/header2.png"), 'Header 2', self, triggered = self.textH2, shortcut='Ctrl+h+2')
        self.header2.setStatusTip('Header 2')

        self.header3 = QAction(QIcon("resources/icons/header3.png"), 'Header 3', self, triggered = self.textH3, shortcut='Ctrl+h+3')
        self.header3.setStatusTip('Header 3')

        self.bold = QAction(QIcon("resources/icons/bold.png"), 'Bold', self, triggered = self.textBold, shortcut = 'Ctrl+n')
        self.bold.setStatusTip('Bold text')

        self.italic = QAction(QIcon("resources/icons/italic.png"), 'Italic', self, triggered = self.textItalic, shortcut = 'Ctrl+k')
        self.italic.setStatusTip('Italic text')

        self.help = QAction('Help', self)
        self.help.setShortcut('Ctrl+h')
        self.help.setStatusTip('Help')

        self.about = QAction('About TextEdit', self)
        self.about.setStatusTip('About TextEdit')

    #Función cerrar que pregunta al usuario si está seguro antes de hacerlo
    def close(self):
        choice = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit TextEdit?', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Si:
            qApp.quit
        else: pass
    
    #Función para abrir el visualizador en HTML del texto en markdown
    def openSubWindow(self):
        filename = os.path.join(CURRENT_DIR, "index.html")

        self.page = PreviewPage()
        self.textPreview.setPage(self.page)

        self.content = Document()
        self.channel = QWebChannel()
        self.channel.registerObject("content", self.content)
        self.page.setWebChannel(self.channel)

        self.textEdit.textChanged.connect(lambda:self.content.set_text(self.textEdit.toPlainText()))

        self.urlMd = urllib.request.pathname2url(os.path.join(os.getcwd(),'index.html'))
        self.textPreview.setUrl(QUrl(self.urlMd))
        
        self.textPreview.load(QUrl.fromLocalFile(filename))

    #Función abrir documento de texto
    def fileOpen(self):
        #Establecemos el archivo que queremos abrir 
        file,_ = QFileDialog.getOpenFileName(self, 'Open file')

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Guardamos la ruta
        self.filePath = file

        name = os.path.basename(self.filePath)
        self.setWindowTitle('%s | TextEdit' %name)

        #Establecemos el widget para escritura y lectura en HTML en paralelo
        self.textEdit = QTextEdit()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.openSubWindow()

        lay = QHBoxLayout(central_widget)
        lay.addWidget(self.textEdit,5)
        lay.addWidget(self.textPreview,5)

        #Abrimos el archivo y guardamos en una variable todo el texto que contiene para mostrarlo
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
            
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
            self.textEdit.setText(text) 

    def fileNew(self):
        #Establecemos el lugar en el que vamos a guardar el archivo
        file,_ = QFileDialog.getSaveFileName(self, 'New file')

        #Añadimos este condicional por si el usuario cancela
        if not file:
            return

        #Guardamos la ruta
        self.filePath = file

        name = os.path.basename(self.filePath)
        self.setWindowTitle('%s | TextEdit' %name)

        #Establecemos el widget para escritura y lectura en HTML en paralelo
        self.textEdit = QTextEdit()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.openSubWindow()

        lay = QHBoxLayout(central_widget)
        lay.addWidget(self.textEdit,5)
        lay.addWidget(self.textPreview,5)

        #Abrimos el archivo con opción de escritura
        if file:
            with open(file, 'w', encoding='utf-8'):
                text = ''
                self.textEdit.setText(text)

    #Función para guardar los cambios
    def fileSave(self):  

        if not self.filePath:
            return

        #Obtengo la ruta del archivo abierto
        file = self.filePath

        #Definimos la función de guardado de un archivo
        with open(file, 'w', encoding='utf-8') as file:
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

    #Función negrita
    def textBold(self):
        tc = self.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('**' + QTextCursor.selectedText(tc) + '**')

    #Función cursiva
    def textItalic(self):
        tc = self.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('*' + QTextCursor.selectedText(tc) + '*')

    #Función h1
    def textH1(self):
        tc = self.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('# ' + QTextCursor.selectedText(tc))

    #Función h2
    def textH2(self):
        tc = self.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('## ' + QTextCursor.selectedText(tc))

    #Función h3
    def textH3(self):
        tc = self.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('### ' + QTextCursor.selectedText(tc))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #Set language
    settings = QtCore.QSettings('TextEdit','SettingsDesktop')
    language = locale.getdefaultlocale()
    settings.value('language',language)
    translation = f'{language}.qm'
    translator = QtCore.QTranslator()
    translator.load(translation,f'resources/i18n/')
    app.installTranslator(translator)

    GUI = MainWindow()
    GUI.show()
    app.exec()

