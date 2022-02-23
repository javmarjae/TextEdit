from typing import Text
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from ..i18n import trans
from controllers.file import FileController
from controllers.textEditingTools import TextEditingTools

class Actions:        

    #Creamos las acciones que se añaden a los menus
    def createActions(self, app):
        self.app = app
        self.tools = TextEditingTools(self.app)
        self.fileController = FileController(self.app)
        
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