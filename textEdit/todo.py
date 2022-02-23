
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
from controllers.textEditingTools import TextEditingTools
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
        self.undoStack = QUndoStack()
        self.undoCommand = QUndoCommand()
        self.setFocus()
        self.fileController = FileController(self)
        self.tools = TextEditingTools(self)
        self._createActions()
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
        fileToolBar = QToolBar(trans('File'),self)
        editToolBar = QToolBar(trans('Edit'),self)

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
        editToolBar.addWidget(self.undoButton)
        editToolBar.addWidget(self.redoButton)

        editToolBar.setMovable(False)
       


    #Creamos las acciones que se añaden a los menus
    def _createActions(self):

        self.newFile = QAction(QIcon("textEdit/resources/icons/newFile.png"),trans('New'), self, triggered = self.fileController.fileNew, shortcut = 'Ctrl+n')
        self.newFile.setStatusTip(trans('New file'))

        self.openFile = QAction(QIcon("textEdit/resources/icons/openFile.png"),trans('Open'), self, triggered = self.fileController.fileOpen, shortcut = 'Ctrl+a')
        self.openFile.setStatusTip(trans('Open file'))

        self.saveFile = QAction(QIcon("textEdit/resources/icons/saveFile.png"),trans('Save'), self, triggered = self.fileController.fileSave, shortcut = 'Ctrl+s')
        self.saveFile.setStatusTip(trans('Save changes'))

        self.closeApp = QAction('Close', self, triggered = self.close, shortcut = 'Ctrl+q')
        self.closeApp.setStatusTip(trans('Close app'))

        self.copyText = QAction(QIcon("textEdit/resources/icons/copy.png"),trans('Copy'), self, triggered = self.tools.textCopy, shortcut = 'Ctrl+c')
        self.copyText.setStatusTip(trans('Copy selected text'))

        self.pasteText = QAction(QIcon("textEdit/resources/icons/paste.png"),trans('Paste'), self, triggered = self.tools.textPaste, shortcut = 'Ctrl+v')
        self.pasteText.setStatusTip(trans('Paste from clipboard'))

        self.cutText = QAction(QIcon("textEdit/resources/icons/cut.png"),trans('Cut'), self, triggered = self.tools.textCut, shortcut = 'Ctrl+x')
        self.cutText.setStatusTip(trans('Cut selected text'))

        self.undoStack.indexChanged.connect(self.fileController.writeFile)

        self.undo = self.undoStack.createUndoAction(self, self.tr('Undo'))
        self.undo.setIcon(QIcon('textEdit/resources/icons/undo.png'))
        self.undo.setShortcut('Ctrl+z')
        #self.undo = QAction(QIcon("resources/icons/undo.png"), 'Undo', self, shortcut = 'Ctrl+z')
        self.undo.setStatusTip('Undo')

        self.undoButton = QToolButton()
        self.undoButton.setText(trans('Undo'))
        self.undoButton.setToolTip(trans('Undo'))
        self.undoButton.setDefaultAction(self.undo)
        self.undoButton.setEnabled(True)
        self.undoButton.setIcon(QIcon('textEdit/resources/icons/undo.png'))
        
        self.redo = self.undoStack.createRedoAction(self, self.tr('Redo'))
        self.redo.setIcon(QIcon('textEdit/resources/icons/redo.png'))
        self.redo.setShortcut('Ctrl+y')
        #self.redo = QAction(QIcon("resources/icons/redo.png"), 'Redo', self, shortcut = 'Ctrl+y')
        self.redo.setStatusTip('Redo')
        #self.redo.triggered.connect(QUndoCommand.redo())

        self.redoButton = QToolButton()
        self.redoButton.setText(trans('Redo'))
        self.redoButton.setToolTip(trans('Redo'))
        self.redoButton.setDefaultAction(self.redo)
        self.redoButton.setEnabled(True)
        self.redoButton.setIcon(QIcon('textEdit/resources/icons/redo.png'))

        self.header1 = QAction(QIcon("textEdit/resources/icons/header1.png"), trans('Header 1'), self, triggered = self.tools.textH1, shortcut='Ctrl+h+1')
        self.header1.setStatusTip(trans('Header 1'))

        self.header2 = QAction(QIcon("textEdit/resources/icons/header2.png"), trans('Header 2'), self, triggered = self.tools.textH2, shortcut='Ctrl+h+2')
        self.header2.setStatusTip(trans('Header 2'))

        self.header3 = QAction(QIcon("textEdit/resources/icons/header3.png"), trans('Header 3'), self, triggered = self.tools.textH3, shortcut='Ctrl+h+3')
        self.header3.setStatusTip(trans('Header 3'))

        self.bold = QAction(QIcon("textEdit/resources/icons/bold.png"), trans('Bold'), self, triggered = self.tools.textBold, shortcut = 'Ctrl+n')
        self.bold.setStatusTip(trans('Bold text'))

        self.italic = QAction(QIcon("textEdit/resources/icons/italic.png"), trans('Italic'), self, triggered = self.tools.textItalic, shortcut = 'Ctrl+k')
        self.italic.setStatusTip(trans('Italic text'))

        self.help = QAction(trans('Help'), self)
        self.help.setShortcut('Ctrl+h')
        self.help.setStatusTip(trans('Help'))

        self.about = QAction(trans('About TextEdit'), self)
        self.about.setStatusTip(trans('About TextEdit'))

    #Función cerrar que pregunta al usuario si está seguro antes de hacerlo
    def close(self):
        choice = QMessageBox.question(self, trans('Exit'), trans('Are you sure you want to exit TextEdit?'), QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Si:
            qApp.quit
        else: pass

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
            text = '**' + QTextCursor.selectedText(tc) + '**'
            tc.insertText(text)

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
    translator.load(translation,f'textEdit/resources/i18n/')
    app.installTranslator(translator)

    GUI = MainWindow()
    GUI.show()
    app.exec()
