
from posixpath import expanduser, normpath
import sys

import os
import locale
from tkinter import Menu
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
from utils.bars import ToolBars, MenuBars
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
        self.menuBars = MenuBars(self)
        self.toolBars = ToolBars(self)

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

