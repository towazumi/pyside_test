# coding:utf-8 

from PySide.QtGui import *

class SimpleOutputWidget(QTextEdit):
    """ シンプルな出力ウィンドウ用ウィジェット """

    def __init__(self, parent=None):
        QTextEdit.__init__(self,parent)
        self.setReadOnly(True)

    def appendText(self, text):
        if not text.endswith('\n'):
            text += '\n' 

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()