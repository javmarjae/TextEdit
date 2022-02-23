from PyQt5.QtWidgets import QMenuBar, QMenu, QToolBar, QSpinBox
from PyQt5.QtCore import Qt

from utils.i18n import trans
from utils.widgets.actions import Actions

from .base import Controller

class MenuBars(Controller):

    def createMenuBar(self):
        self.actions = Actions(self.app)

        menuBar = QMenuBar(self)

        #Añadimos los tres menus: archivo, editar y ayuda
        fileMenu = QMenu(trans("File"), self)
        editMenu = QMenu(trans("Edit"), self)
        helpMenu = QMenu(trans("Help"), self)

        #Añadimos el menu archivo con sus acciones
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.actions.newFile)
        fileMenu.addAction(self.actions.openFile)
        fileMenu.addAction(self.actions.saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actions.closeApp)

        #Añadimos el menu editar con sus acciones
        menuBar.addMenu(editMenu)
        editMenu.addAction(self.actions.copyText)
        editMenu.addAction(self.actions.pasteText)
        editMenu.addAction(self.actions.cutText)
        editMenu.addSeparator()
        #editMenu.addAction(self.undo)
        #editMenu.addAction(self.redo)

        #Añadimos el menu ayuda con sus acciones
        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.actions.help)
        helpMenu.addSeparator()
        helpMenu.addAction(self.actions.about)

        self.setMenuBar(menuBar)

class ToolBars(Controller):

    def createToolBars(self):
        self.actions = Actions(self.app)

        fileToolBar = QToolBar(trans('File'),self)
        editToolBar = QToolBar(trans('Edit'),self)

        self.app.addToolBar(fileToolBar)
        self.app.addToolBar(editToolBar)

        fileToolBar.addAction(self.actions.newFile)
        fileToolBar.addAction(self.actions.openFile)
        fileToolBar.addAction(self.actions.saveFile)

        fileToolBar.setMovable(False)

        editToolBar.addAction(self.actions.copyText)
        editToolBar.addAction(self.actions.pasteText)
        editToolBar.addAction(self.actions.cutText)
        editToolBar.addSeparator()
        self.fontSizeBox = QSpinBox()
        self.fontSizeBox.setFocusPolicy(Qt.NoFocus)
        editToolBar.addWidget(self.fontSizeBox)
        editToolBar.addAction(self.actions.bold)
        editToolBar.addAction(self.actions.italic)
        editToolBar.addSeparator()
        editToolBar.addAction(self.actions.header1)
        editToolBar.addAction(self.actions.header2)
        editToolBar.addAction(self.actions.header3)
        editToolBar.addSeparator()
        #editToolBar.addWidget(self.undoButton)
        #editToolBar.addWidget(self.redoButton)

        editToolBar.setMovable(False)