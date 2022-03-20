
from posixpath import expanduser, normpath
import sys

import os
import locale

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import Qt, pyqtProperty, QFile, QTextStream
from utils.i18n import trans
from utils.commands import *
from controllers.views import ViewsController
from controllers.file import FileController
from controllers.text import TextEditingTools
from utils.bars import ToolBars, MenuBars
from utils.widgets.actions import Actions

#Para documentar el código, se debe descomentar la linea superior y comentar la inferior
#Ui_MainWindow, QtBaseClass = uic.loadUiType(os.path.join(os.getcwd(),'..\\textEdit\\resources\\ui\\mainwindow.ui'))
Ui_MainWindow, QtBaseClass = uic.loadUiType(os.path.join(os.getcwd(),'textEdit\\resources\\ui\\mainwindow.ui'))

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
        self.clipboard = QApplication.clipboard()
        self.statusBar = QStatusBar()
        self.cursor = QtGui.QTextCursor()
        self.setFocus()
        self.fileController = FileController(self)
        self.tools = TextEditingTools(self)
        self.createActions = Actions(self)
        self.menuBars = MenuBars(self)
        self.toolBars = ToolBars(self)
        #Establezco que no se pueda escribir hasta que se abra o cree un archivo
        self.textEdit.setReadOnly(True)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QHBoxLayout(central_widget)
        lay.addWidget(self.textEdit,5)
        lay.addWidget(self.textPreview,5)

    #Función cerrar que pregunta al usuario si está seguro antes de hacerlo
    def close(self):
        choice = QMessageBox.question(self, trans('Exit'), trans('Are you sure you want to exit TextEdit?'), QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Si:
            qApp.quit
        else: pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #Establecemos el idioma
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

