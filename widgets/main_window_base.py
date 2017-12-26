#coding: utf-8

from PySide.QtCore import *
from PySide.QtGui import *

class MainWindowBase(QMainWindow):

    def __init__(self,parent=None):
        QMainWindow.__init__(self,parent)


    def createAction(self, text, triggered=None, shortcut=None, icon=None, tip=None):
        """ アクションの生成 """
        action = QAction(text, self)
        if triggered is not None:
            action.triggered.connect(triggered)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(QIcon(':/{0}.png'.format(icon)))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        return action

    def createDockWidget(self, widget_type, title, area):
        """ ドックにウィジェットを配置してそのウィジェットを返す """
        dock = QDockWidget(title, self)
        widget = widget_type(dock)
        dock.setWidget(widget)
        self.addDockWidget(area, dock)
        return widget
