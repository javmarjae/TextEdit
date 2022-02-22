from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal

class Document(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_text = ''

    def get_text(self):
        return self.m_text

    def set_text(self, text):
        if self.m_text == text:
            return
        self.m_text = text
        self.textChanged.emit(self.m_text)

    textChanged = pyqtSignal(str)
    text = pyqtProperty(str, fget=get_text, fset=set_text, notify=textChanged)