# coding:utf-8 

from Qt import QtGui, QtWidgets, QtCore

class SimpleOutputWidget(QtWidgets.QTextEdit):
    """ シンプルな出力ウィンドウ用ウィジェット """

    def __init__(self, parent=None):
        QtWidgets.QTextEdit.__init__(self,parent)
        self.setReadOnly(True)

    def appendText(self, text):
        if not text.endswith('\n'):
            text += '\n' 

        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()