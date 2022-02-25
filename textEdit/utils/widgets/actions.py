from typing import Text
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from ..i18n import trans
from controllers.file import FileController
from controllers.text import TextEditingTools

class Actions:        

    def __init__(self, app):
        self.app = app
        self.tools = TextEditingTools(self.app)
        self.fileController = FileController(self.app)

        #Creamos la acción para archivos nuevos
        self.newFile = QAction()
        self.newFile.setIcon(QIcon("textEdit/resources/icons/newFile.png"))
        self.newFile.setText(trans('New'))
        self.newFile.setShortcut('Ctrl+n')
        self.newFile.triggered.connect(self.fileController.fileNew)
        self.newFile.setStatusTip(trans('New file'))

        #Creamos la acción para abrir archivos
        self.openFile = QAction()
        self.openFile.setIcon(QIcon("textEdit/resources/icons/openFile.png"))
        self.openFile.setText(trans('Open'))
        self.openFile.setShortcut('Ctrl+a')
        self.openFile.triggered.connect(self.fileController.fileOpen)
        self.openFile.setStatusTip(trans('Open file'))

        #Creamos la acción para guardar cambios
        self.saveFile = QAction()
        self.saveFile.setIcon(QIcon("textEdit/resources/icons/saveFile.png"))
        self.saveFile.setText(trans('Save'))
        self.saveFile.setShortcut('Ctrl+s')
        self.saveFile.triggered.connect(self.fileController.fileSaveChanges)
        self.saveFile.setStatusTip(trans('Save changes'))

        #Creamos la acción para cerrar la app
        self.closeApp = QAction()
        self.closeApp.setText(trans('Close'))
        self.closeApp.setShortcut('Ctrl+q')
        self.closeApp.triggered.connect(self.app.close)
        self.closeApp.setStatusTip(trans('Close app'))

        #Creamos la acción para copiar texto
        self.copyText = QAction()
        self.copyText.setIcon(QIcon("textEdit/resources/icons/copy.png"))
        self.copyText.setText(trans('Copy'))
        self.copyText.setShortcut('Ctrl+c')
        self.copyText.triggered.connect(self.tools.textCopy)
        self.copyText.setStatusTip(trans('Copy selected text'))

        #Creamos la acción para pegar texto
        self.pasteText = QAction()
        self.pasteText.setIcon(QIcon("textEdit/resources/icons/paste.png"))
        self.pasteText.setText(trans('Paste'))
        self.pasteText.setShortcut('Ctrl+v')
        self.pasteText.triggered.connect(self.tools.textPaste)
        self.pasteText.setStatusTip(trans('Paste from clipboard'))

        #Creamos la acción para cortar texto
        self.cutText = QAction()
        self.cutText.setIcon(QIcon("textEdit/resources/icons/cut.png"))
        self.cutText.setText(trans('Cut'))
        self.cutText.setShortcut('Ctrl+x')
        self.cutText.triggered.connect(self.tools.textCut)
        self.cutText.setStatusTip(trans('Cut selected text'))

        '''

        self.undoStack.indexChanged.connect(self.writeFile)

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

        '''

        #Creamos la acción para establecer un texto como título grande
        self.header1 = QAction()
        self.header1.setIcon(QIcon("textEdit/resources/icons/header1.png"))
        self.header1.setText(trans('Header 1'))
        self.header1.setShortcut('Ctrl+h+1')
        self.header1.triggered.connect(self.tools.textH1)
        self.header1.setStatusTip(trans('Header 1'))

        #Creamos la acción para establecer un texto como título mediano
        self.header2 = QAction()
        self.header2.setIcon(QIcon("textEdit/resources/icons/header2.png"))
        self.header2.setText(trans('Header 2'))
        self.header2.setShortcut('Ctrl+h+2')
        self.header2.triggered.connect(self.tools.textH2)
        self.header2.setStatusTip(trans('Header 2'))

        #Creamos la acción para establecer un texto como título pequeño
        self.header3 = QAction()
        self.header3.setIcon(QIcon("textEdit/resources/icons/header3.png"))
        self.header3.setText(trans('Header 3'))
        self.header3.setShortcut('Ctrl+h+3')
        self.header3.triggered.connect(self.tools.textH3)
        self.header3.setStatusTip(trans('Header 3'))

        #Creamos la acción para establecer un texto como marcado
        self.bold = QAction()
        self.bold.setIcon(QIcon("textEdit/resources/icons/bold.png"))
        self.bold.setText(trans('Bold'))
        self.bold.setShortcut('Ctrl+n')
        self.bold.triggered.connect(self.tools.textBold)
        self.bold.setStatusTip(trans('Bold text'))

        #Creamos la acción para establecer un texto como cursiva
        self.italic = QAction()
        self.italic.setIcon(QIcon("textEdit/resources/icons/italic.png"))
        self.italic.setText(trans('Italic'))
        self.italic.setShortcut('Ctrl+k')
        self.italic.triggered.connect(self.tools.textItalic)
        self.italic.setStatusTip(trans('Italic text'))

        #Creamos la acción ayuda, sin funcionalidad de momento
        self.help = QAction()
        self.help.setText(trans('Help'))
        self.help.setShortcut('Ctrl+h')
        self.help.setStatusTip(trans('Help'))

        #Creamos la acción acerca de la aplicación
        self.about = QAction()
        self.about.setText(trans('About...'))
        self.about.setStatusTip(trans('About TextEdit'))