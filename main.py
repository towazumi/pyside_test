# coding:utf-8 

import os
import sys
import json

import logging
import logging.config

from PySide.QtCore import *
from PySide.QtGui import *

from log import SignalLogHandler
from widgets import SimpleOutputWidget, TreeModel, TreeItem


def get_style(style_name):
    """ スタイルのファイル内容を取得 """
    try:
        style_file = os.path.join(
            os.path.dirname(__file__), 'style', '{}.qss'.format(style_name) )
        with open(style_file, 'r') as f:
            style = f.read()
    except:
        print('not found')
        style = ''
    return style

class TestBaseItem(TreeItem):

    HEADER_ITEMS = (u'名前',u'値')

    def __init__(self, parent):
        TreeItem.__init__(self,parent)

    def columnCount(self):
        return len(self.HEADER_ITEMS)

    def headerData(self,column):
        return self.HEADER_ITEMS[column]

class GroupItem(TestBaseItem):

    def __init__(self, parent, name):
        TestBaseItem.__init__(self, parent)
        self.name = name

    def data(self, column):
        if 0==column:
            return self.name
        else:
            return None

class TestItem(TestBaseItem):
    def __init__(self, parent, name, value):
        TestBaseItem.__init__(self,parent)
        self.name = name
        self.value = value

    def data(self,column):
        if 0==column:
            return self.name
        elif 1==column:
            return self.value
        else:
            None


class TestWindow(QMainWindow):
    """ テストウィンドウ """

    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)

        # ツリービュー
        treeView = QTreeView(self)
        treeModel = TreeModel(treeView)
        treeView.setModel(treeModel)
        group = GroupItem( treeModel.root, u'テストグループ' )
        TestItem(group, u'テスト', 3)
        self.setCentralWidget(treeView)

        # 履歴
        historyDock = QDockWidget(u'履歴', self)
        historyView = QUndoView(historyDock)
        historyDock.setWidget(historyView)
        self.addDockWidget(Qt.RightDockWidgetArea, historyDock)
    
        # 出力
        outputDock = QDockWidget(u'出力', self)
        outputWidget = SimpleOutputWidget(outputDock)
        outputDock.setWidget(outputWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, outputDock)

        SignalLogHandler.connect(outputWidget.appendText)

def main():

    # ログ設定
    logging.handlers.SignalLogHandler = SignalLogHandler
    logging.config.fileConfig('log/logging.conf')

    # create logger
    logger = logging.getLogger('app')

    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

    # アプリケーション
    app = QApplication(sys.argv)
    app.setStyleSheet(get_style('dark'))
    
    windowA = TestWindow()
    windowA.setWindowTitle('WindowA')
    windowA.resize(640, 480)
    windowA.show()

    logger.debug('test')
    logger.debug('test')

    sys.exit(app.exec_())


if __name__=='__main__':
    main()
