from PyQt5.QtGui import QIcon, QTextCursor 

from .base import Controller

class TextEditingTools(Controller):

    def __init__(self, app):
        super().__init__(app)

    #Función copiar
    def textCopy(self):
        tc = self.app.textEdit.textCursor()
        text = QTextCursor.selectedText(tc)
        self.app.clipboard.setText(text)

    #Función pegar
    def textPaste(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            QTextCursor.removeSelectedText(tc)
        tc.insertText(self.app.clipboard.text())
    
    #Función cortar
    def textCut(self):
        tc = self.app.textEdit.textCursor()
        text = QTextCursor.selectedText(tc)
        self.app.clipboard.setText(text)
        QTextCursor.removeSelectedText(tc)

    #Función negrita
    def textBold(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            text = '**' + QTextCursor.selectedText(tc) + '**'
            tc.insertText(text)

    #Función cursiva
    def textItalic(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('*' + QTextCursor.selectedText(tc) + '*')

    #Función h1
    def textH1(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('# ' + QTextCursor.selectedText(tc))

    #Función h2
    def textH2(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('## ' + QTextCursor.selectedText(tc))  

    #Función h3
    def textH3(self):
        tc = self.app.textEdit.textCursor()
        if QTextCursor.selectedText(tc) != '':
            tc.insertText('### ' + QTextCursor.selectedText(tc))