from stat import filemode
from PyQt5.QtWidgets import QMenuBar, QMenu, QToolBar, QSpinBox
from PyQt5.QtCore import Qt

from utils.i18n import trans
from utils.widgets.actions import Actions



class MenuBars:
    """
        Creating the menu bars that are showed
        in the app

    """

    def __init__(self,app):
        self.app = app
        self.actions = Actions(self.app)
        self.createMenuBar()

    def createMenuBar(self):
        
        menuBar = QMenuBar(self.app)

        fileMenu = QMenu(trans('File'), self.app)
        editMenu = QMenu(trans('Edit'), self.app)
        helpMenu = QMenu(trans('Help'), self.app)

        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.actions.newFile)
        fileMenu.addAction(self.actions.openFile)
        fileMenu.addAction(self.actions.saveFile)
        fileMenu.addAction(self.actions.saveAs)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actions.closeApp)

        menuBar.addMenu(editMenu)
        editMenu.addAction(self.actions.copyText)
        editMenu.addAction(self.actions.pasteText)
        editMenu.addAction(self.actions.cutText)
        editMenu.addSeparator()
        editMenu.addAction(self.actions.undo)
        editMenu.addAction(self.actions.redo)
        editMenu.addSeparator()
        editMenu.addAction(self.actions.toggleTheme)
        
        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.actions.help)
        helpMenu.addSeparator()
        helpMenu.addAction(self.actions.about)

        self.app.setMenuBar(menuBar)



class ToolBars:
    """
        Creating the tool bars that are showed
        in the app

    """

    def __init__(self,app):
        self.app = app
        self.actions = Actions(self.app)
        self.createToolBars()

    def createToolBars(self):      

        fileToolBar = QToolBar(trans('File'), self.app)
        editToolBar = QToolBar(trans('Edit'), self.app)

        self.app.addToolBar(fileToolBar)
        self.app.addToolBar(editToolBar)

        fileToolBar.addAction(self.actions.newFile)
        fileToolBar.addAction(self.actions.openFile)
        fileToolBar.addAction(self.actions.saveFile)
        fileToolBar.addAction(self.actions.saveAs)

        fileToolBar.setMovable(False)

        editToolBar.addAction(self.actions.copyText)
        editToolBar.addAction(self.actions.pasteText)
        editToolBar.addAction(self.actions.cutText)
        editToolBar.addSeparator()
        editToolBar.addAction(self.actions.bold)
        editToolBar.addAction(self.actions.italic)
        editToolBar.addSeparator()
        editToolBar.addAction(self.actions.header1)
        editToolBar.addAction(self.actions.header2)
        editToolBar.addAction(self.actions.header3)
        editToolBar.addSeparator()
        editToolBar.addAction(self.actions.undo)
        editToolBar.addAction(self.actions.redo)
        editToolBar.addSeparator()
        editToolBar.addAction(self.actions.toggleTheme)

        editToolBar.setMovable(False)