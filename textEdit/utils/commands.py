from PyQt5.QtWidgets import QUndoCommand, QTextEdit

class CreateObject(QUndoCommand):

    def __init__(self, text, document):
        super(CreateObject,self).__init__()
        self.m_text = text
        self.m_doc = document

    def undo(self):
        self.m_doc.replace(self.m_text,'')

    def redo(self):
        self.m_doc.insertPlainText(self.m_text)

class Cut(QUndoCommand):
    def __init__(self,text,document):
        super(Cut,self).__init__()
        self.m_text = text
        self.m_doc = document

    def undo(self):
        self.m_doc.insertPlainText(self.m_text)

    def redo(self):
        self.m_doc.repalce(self.m_text, '')