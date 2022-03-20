import os
import urllib.request
import sys

from .base import Controller
from .document import Document
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import *

class PreviewPage(QWebEnginePage):
    pass

class ViewsController(Controller):

    def __init__(self, app):
        super().__init__(app)

    def toggleStyleSheet():
        """
        This function toggles the app theme
        between dark and light

        """
        if(qApp.styleSheet() != open("textEdit/resources/themes/light.qss","r").read()):
            qApp.setStyleSheet(open("textEdit/resources/themes/light.qss","r").read())
        else:
            qApp.setStyleSheet(open("textEdit/resources/themes/dark.qss","r").read())
    
    def openSubWindow(self):
        """
        This function shows the markdown text provided by
        the user in a parallel window transformed to
        HTML in real time

        """

        filename = os.path.join(os.getcwd(),'textEdit\\resources\\html\\index.html')

        self.page = PreviewPage()
        self.app.textPreview.setPage(self.page)
        
        self.content = Document()
        self.channel = QWebChannel()
        self.channel.registerObject("content", self.content)
        self.page.setWebChannel(self.channel)

        self.app.textEdit.textChanged.connect(lambda:self.content.set_text(self.app.textEdit.toPlainText()))

        self.urlMd = urllib.request.pathname2url(os.path.join(os.getcwd(),'textEdit\\resources\\html\\index.html'))
        self.app.textPreview.setUrl(QUrl(self.urlMd))
        
        self.app.textPreview.load(QUrl.fromLocalFile(filename))