from stat import filemode
from PyQt5.QtWidgets import QMenuBar, QMenu, QToolBar, QSpinBox
from PyQt5.QtCore import Qt

from utils.i18n import trans
from utils.widgets.actions import Actions



class MenuBars:

    def __init__(self,app):
        self.app = app
        self.actions = Actions(self.app)
        self.createMenuBar()

    def createMenuBar(self):
        #Creamos el menuBar y el parent
        menuBar = QMenuBar(self.app)

        #Añadimos los tres menus: archivo, editar y ayuda
        fileMenu = QMenu(trans('File'), self.app)
        editMenu = QMenu(trans('Edit'), self.app)
        helpMenu = QMenu(trans('Help'), self.app)

        #Añadimos el menu archivo con sus acciones
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.actions.newFile)
        fileMenu.addAction(self.actions.openFile)
        fileMenu.addAction(self.actions.saveFile)
        fileMenu.addAction(self.actions.saveAs)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actions.closeApp)

        #Añadimos el menu editar con sus acciones
        menuBar.addMenu(editMenu)
        editMenu.addAction(self.actions.copyText)
        editMenu.addAction(self.actions.pasteText)
        editMenu.addAction(self.actions.cutText)
        editMenu.addSeparator()
        editMenu.addAction(self.actions.undo)
        editMenu.addAction(self.actions.redo)
        editMenu.addSeparator()
        editMenu.addAction(self.actions.toggleTheme)
        
        #Añadimos el menu ayuda con sus acciones
        menuBar.addMenu(helpMenu)
        helpMenu.addAction(self.actions.help)
        helpMenu.addSeparator()
        helpMenu.addAction(self.actions.about)

        #Establecemos el menuBar dentro de la appp
        self.app.setMenuBar(menuBar)



class ToolBars:

    def __init__(self,app):
        self.app = app
        self.actions = Actions(self.app)
        self.createToolBars()

    def createToolBars(self):      

        #Creamos ambas barras de herramientas con la app como parent
        fileToolBar = QToolBar(trans('File'), self.app)
        editToolBar = QToolBar(trans('Edit'), self.app)

        #Las añadimos
        self.app.addToolBar(fileToolBar)
        self.app.addToolBar(editToolBar)

        #Añadimos las acciones deseadas
        fileToolBar.addAction(self.actions.newFile)
        fileToolBar.addAction(self.actions.openFile)
        fileToolBar.addAction(self.actions.saveFile)
        fileToolBar.addAction(self.actions.saveAs)

        #Establecemos que esté fija
        fileToolBar.setMovable(False)

        #Añadimos las acciones deseadas y las separamos mediante separadores
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

        #Establecemos que esté fija
        editToolBar.setMovable(False)