# coding:utf-8 

import os
import sys

import logging
import logging.config

from PySide.QtCore import *
from PySide.QtGui import *

from log import SignalLogHandler
from widgets import MainWindowBase, NodeBase, NodeScene

class TestNode(NodeBase):

    def __init__(self, parent=None, scene=None):
        NodeBase.__init__(self,parent,scene)

        self.size = QSize(140.0,80.0)

        self.input_attributes = ['in_node1', 'in_node2']
        self.output_attributes = ['out_node']

        self.setupEdgePoints()

class TestNodeOutputOnly(NodeBase):

    def __init__(self, parent=None, scene=None):
        NodeBase.__init__(self,parent,scene)

        self.size = QSize(140.0,80.0)

        self.output_attributes = ['output']

        self.setupEdgePoints()

class TestNodeInputOnly(NodeBase):

    def __init__(self, parent=None, scene=None):
        NodeBase.__init__(self,parent,scene)

        self.size = QSize(140.0,80.0)

        self.input_attributes = ['input']

        self.setupEdgePoints()



class TestWindow(MainWindowBase):
    """ テストウィンドウ """

    def __init__(self, parent=None):
        MainWindowBase.__init__(self,parent)

        graphicsView = QGraphicsView(self)
        scene = NodeScene(graphicsView)
        scene.setBackgroundBrush( QBrush(QColor(0,0,0)) )
        graphicsView.setScene(scene)

        scene.addItem(TestNode())
        scene.addItem(TestNodeInputOnly())
        scene.addItem(TestNodeOutputOnly())

        self.setCentralWidget(graphicsView)


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

def main():

    # ログ設定
    logging.handlers.SignalLogHandler = SignalLogHandler
    logging.config.fileConfig('log/logging.conf')

    # アプリケーション
    app = QApplication(sys.argv)
    app.setStyleSheet(get_style('dark'))
    
    window = TestWindow()
    window.setWindowTitle('PysideTestApplication')
    window.resize(640, 480)
    window.show()

    sys.exit(app.exec_())


if __name__=='__main__':
    main()

