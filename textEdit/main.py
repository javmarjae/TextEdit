
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

    def __init__(self):
        super(QMainWindow,self).__init__(parent=None)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.setWindowIcon(QIcon("textEdit/resources/icons/icon.png"))
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
        self.textEdit.setText("Abra o cree un nuevo archivo para empezar a redactar.")
        
        self.textEdit.setReadOnly(True)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        lay = QHBoxLayout(central_widget)
        lay.addWidget(self.textEdit,5)
        lay.addWidget(self.textPreview,5)

    def close(self):
        choice = QMessageBox.question(self, trans('Exit'), trans('Are you sure you want to exit TextEdit?'), QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Si:
            qApp.quit
        else: pass

if __name__ == '__main__':
    app = QApplication(sys.argv)

    """
    Stablish the app language depending
    on the system's language

    """
    settings = QtCore.QSettings('TextEdit','SettingsDesktop')
    language = locale.getdefaultlocale()
    settings.value('language',language)
    translation = f'{language}.qm'
    translator = QtCore.QTranslator()
    translator.load(translation,f'textEdit/resources/i18n/')
    app.installTranslator(translator)

    GUI = MainWindow()
    total_size = GUI.screen().availableGeometry()
    GUI.resize(total_size.width()*2/3, total_size.height()*2/3)
    GUI.showMaximized()
    app.exec()

