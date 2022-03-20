from PyQt5.QtGui import QIcon, QTextCursor 

from .base import Controller

class TextEditingTools(Controller):
    """
        Creating the basic functions that allows
        the user to do the basic things with the 
        text using the buttons located at the menu
        or the tool bars

    """

    def __init__(self, app):
        super().__init__(app)

    def textCopy(self):
        tc = self.app.textEdit.textCursor()
        text = QTextCursor.selectedText(tc)
        self.app.clipboard.setText(text)

    def textPaste(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            QTextCursor.removeSelectedText(tc)
        tc.insertText(self.app.clipboard.text())
    
    def textCut(self):
        tc = self.app.textEdit.textCursor()
        text = QTextCursor.selectedText(tc)
        self.app.clipboard.setText(text)
        QTextCursor.removeSelectedText(tc)

    def textBold(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            text = '**' + QTextCursor.selectedText(tc) + '**'
            tc.insertText(text)

    def textItalic(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('*' + QTextCursor.selectedText(tc) + '*')

    def textH1(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('# ' + QTextCursor.selectedText(tc))

    def textH2(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('## ' + QTextCursor.selectedText(tc))  

    def textH3(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('### ' + QTextCursor.selectedText(tc))