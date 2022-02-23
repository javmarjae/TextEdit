
from posixpath import expanduser, normpath
import sys

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
from PyQt5.QtWebChannel import QWebChannel
from utils.i18n import trans
from utils.commands import *
from controllers.views import ViewsController
from controllers.file import FileController
from controllers.text import TextEditingTools
from controllers.bars import ToolBars, MenuBars
from utils.widgets.actions import Actions

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

qt_creator_file = "textEdit\mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class MainWindow(QMainWindow, Ui_MainWindow):

    #Inicializamos
    def __init__(self):
        super(QMainWindow,self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.views = ViewsController(self)
        self.textPreview = QWebEngineView()
        self.textPreview.setContextMenuPolicy(Qt.NoContextMenu)
        self.textEdit = QTextEdit()
        self.lineEdit = QLineEdit()
        self.clipboard = QApplication.clipboard()
        self.statusBar = QStatusBar()
        self.cursor = QtGui.QTextCursor()
        self.setFocus()
        self.fileController = FileController(self)
        self.tools = TextEditingTools(self)
        self.createActions = Actions(self)
        self._createMenuBar()
        self._createToolBars()

    #Creamos la barra de menu
    def _createMenuBar(self):
        menuBar = QMenuBar(self)

        #Añadimos los tres menus: archivo, editar y ayuda
        fileMenu = QMenu(trans("File"), self)
        editMenu = QMenu(trans("Edit"), self)
        helpMenu = QMenu(trans("Help"), self)

        #Añadimos el menu archivo con sus acciones
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.createActions.newFile)
        fileMenu.addAction(self.createActions.openFile)
        fileMenu.addAction(self.createActions.saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(self.createActions.closeApp)

        #Añadimos el menu editar con sus acciones
        menuBar.addMenu(editMenu)
        editMenu.addAction(self.createActions.copyText)
        editMenu.addAction(self.createActions.pasteText)
        editMenu.addAction(self.createActions.cutText)
        editMenu.addSeparator()
        #editMenu.addAction(self.undo)
        #editMenu.addAction(self.redo)

        #Añadimos el menu ayuda con sus acciones
        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.createActions.help)
        helpMenu.addSeparator()
        helpMenu.addAction(self.createActions.about)

        self.setMenuBar(menuBar)

    #Creamos la barra de herramientas
    def _createToolBars(self):
        fileToolBar = QToolBar(trans('File'),self)
        editToolBar = QToolBar(trans('Edit'),self)

        self.addToolBar(fileToolBar)
        self.addToolBar(editToolBar)

        fileToolBar.addAction(self.createActions.newFile)
        fileToolBar.addAction(self.createActions.openFile)
        fileToolBar.addAction(self.createActions.saveFile)

        fileToolBar.setMovable(False)

        editToolBar.addAction(self.createActions.copyText)
        editToolBar.addAction(self.createActions.pasteText)
        editToolBar.addAction(self.createActions.cutText)
        editToolBar.addSeparator()
        self.fontSizeBox = QSpinBox()
        self.fontSizeBox.setFocusPolicy(Qt.NoFocus)
        editToolBar.addWidget(self.fontSizeBox)
        editToolBar.addAction(self.createActions.bold)
        editToolBar.addAction(self.createActions.italic)
        editToolBar.addSeparator()
        editToolBar.addAction(self.createActions.header1)
        editToolBar.addAction(self.createActions.header2)
        editToolBar.addAction(self.createActions.header3)
        editToolBar.addSeparator()
        #editToolBar.addWidget(self.undoButton)
        #editToolBar.addWidget(self.redoButton)

        editToolBar.setMovable(False)

    #Función cerrar que pregunta al usuario si está seguro antes de hacerlo
    def close(self):
        choice = QMessageBox.question(self, trans('Exit'), trans('Are you sure you want to exit TextEdit?'), QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Si:
            qApp.quit
        else: pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #Set language
    settings = QtCore.QSettings('TextEdit','SettingsDesktop')
    language = locale.getdefaultlocale()
    settings.value('language',language)
    translation = f'{language}.qm'
    translator = QtCore.QTranslator()
    translator.load(translation,f'textEdit/resources/i18n/')
    app.installTranslator(translator)

    GUI = MainWindow()
    GUI.show()
    app.exec()

