import os
import urllib.request

from .base import Controller
from .document import Document
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl

DIR = os.path.dirname(os.path.realpath(__file__))

class PreviewPage(QWebEnginePage):
    pass

class ViewsController(Controller):

    def __init__(self, app):
        super().__init__(app)
    
    #Función para abrir el visualizador en HTML del texto en markdown
    def openSubWindow(self):
        filename = os.path.join(DIR, "index.html")

        self.page = PreviewPage()
        self.app.textPreview.setPage(self.page)
        
        self.content = Document()
        self.channel = QWebChannel()
        self.channel.registerObject("content", self.content)
        self.page.setWebChannel(self.channel)

        self.app.textEdit.textChanged.connect(lambda:self.content.set_text(self.app.textEdit.toPlainText()))

        self.urlMd = urllib.request.pathname2url(os.path.join(os.getcwd(),'index.html'))
        self.app.textPreview.setUrl(QUrl(self.urlMd))
        
        self.app.textPreview.load(QUrl.fromLocalFile(filename))