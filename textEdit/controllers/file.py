import os
from .base import Controller

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFileDialog
from utils.i18n import trans


class FileController(Controller):
    def __init__(self, app):
        super().__init__(app)
        self.filePath = ''

    def fileOpen(self): 
        """
        This function allows the user to open a file

        """
        file,_ = QFileDialog.getOpenFileName(self.app, trans('Open file'))

        if not file:
            return

        self.filePath = file

        name = os.path.basename(self.filePath)
        self.app.setWindowTitle('%s | TextEdit' %name)

        self.app.views.openSubWindow()  

        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
        self.writeFile(file, text)
        
    def fileNew(self):
        """
        This function allows the user to create a new file
        stablishing where does the user want to save it

        """
        file,_ = QFileDialog.getSaveFileName(self.app, trans('New file'))

        if not file:
            return

        self.filePath = file

        name = os.path.basename(self.filePath)
        self.app.setWindowTitle('%s | TextEdit' %name)

        self.app.views.openSubWindow()      

        self.writeFile(file, text = '')
        
    def writeFile(self,file,text):
        """
        This function allows the user to edit a file

        """
        self.app.textEdit.setReadOnly(False)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(text)
            self.app.textEdit.setText(text)
            
    def fileSaveChanges(self):  
        """
        This function allows the user to save the changes
        in the opened file

        """
        if not self.filePath:
            return

        with open(self.filePath, 'w', encoding='utf-8') as f:
            text = self.app.textEdit.toPlainText()
            f.write(text)
    
    def saveAs(self):
        """
        This function allows the user to save a file
        using a different name or path

        """
        file,_ = QFileDialog.getSaveFileName(self.app, trans('New file'))

        if not file:
            return

        with open(file, 'w', encoding='utf-8') as f:
            text = self.app.textEdit.toPlainText()
            f.write(text)