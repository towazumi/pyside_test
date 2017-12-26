# coding:utf-8 

import os
import sys
import json
import codecs

import logging
import logging.config

from PySide.QtCore import *
from PySide.QtGui import *

from log import SignalLogHandler
from widgets import SimpleOutputWidget, MainWindowBase, TreeModel, TreeItem, TreeView

class OutputCapture(QObject):
    emitter = Signal(str)
    def __init__(self, parent=None):
        QObject.__init__(self,parent)
    def write(self, string):
        self.emitter.emit(string)

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

class Test:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def serialize(self):
        return [self.x, self.y]
    def deserialize(self, data, proto_types):
        self.x = data[0]
        self.y = data[1]
    

class TestBaseItem(TreeItem):

    ITEMS = [
        (u'name',u'名前'),
        (u'value',u'値')
    ]

    def __init__(self, parent):
        TreeItem.__init__(self,parent)

    def columnCount(self):
        return len(self.ITEMS)

    def headerData(self,column):
        return self.ITEMS[column][1]

    def editable(self, column):
        attr =  self.ITEMS[column][0]
        return hasattr(self, attr)

    def data(self,column):
        attr =  self.ITEMS[column][0]
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            return None

    def setData(self, column, value):
        attr =  self.ITEMS[column][0]
        if hasattr(self, attr):
            setattr(self, attr, value)
            return True 
        else:
            return False


class GroupItem(TestBaseItem):
    def __init__(self, parent=None, name=None):
        TestBaseItem.__init__(self, parent)
        self.name = name

    def data(self, column):
        if 0==column:
            return self.name
        else:
            return None

class TestItem(TestBaseItem):
    def __init__(self, parent=None, name=None, value=0):
        TestBaseItem.__init__(self,parent)
        self.name = name
        self.value = value
        self.test = Test(1,2)

class TestWindow(MainWindowBase):
    """ テストウィンドウ """

    def __init__(self, parent=None):
        MainWindowBase.__init__(self,parent)
        
        self.__filename = None

        self.proto_types = dict(
            GroupItem = GroupItem(),
            TestItem = TestItem()
        )

        openAction = self.createAction(
            text='Open',
            triggered=self.openFile,
            shortcut='Ctrl+O',
            tip='Open file'
        )
        saveAction = self.createAction(
            text='Save As',
            triggered=self.saveFile,
            shortcut='Ctrl+S',
            tip='Save file'
        )
        saveAsAction = self.createAction(
            text='Save As',
            triggered=self.saveFileAs,
            shortcut='Ctrl+Shift+S',
            tip='Save file as new file name'
        )
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)

        # ツリービュー
        treeView = TreeView(self)
        treeModel = TreeModel(treeView)
        treeView.setModel(treeModel)
        """
        group = GroupItem( treeModel.root, u'テストグループ' )
        TestItem(group, u'テスト', 3)
        group2 = GroupItem( treeModel.root, u'テストグループ2' )
        TestItem(group2, u'テスト2', 6)
        TestItem(group2, u'テスト3', 9)
        """
        self.setCentralWidget(treeView)

        self.treeModel = treeModel

        # 履歴
        self.createDockWidget( QUndoView, u'履歴', Qt.RightDockWidgetArea)
    
        # 出力
        outputWidget = self.createDockWidget(SimpleOutputWidget, u'出力', Qt.BottomDockWidgetArea)
        SignalLogHandler.connect(outputWidget.appendText)

    def openFile(self):
        """ファイルを開く"""
        directory = os.path.dirname(self.__filename) if self.__filename else os.getcwd()
        filetuple = QFileDialog.getOpenFileName(self,'Open File', directory, 'Json (*.json)\nAll Files (*.*)')
        filename = filetuple[0]
        if len(filename)>0:
            with codecs.open(filename,'r','utf-8') as f:
                data = json.load(f)
            self.__filename = filename

            self.setWindowTitle(u'PysideTestApplication [{0}]'.format(filename))
            self.treeModel.deserialize(data,self.proto_types)

    def saveFile(self):
        """保存"""
        if self.__filename:
            self.__save(self.__filename)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        """名前を付けて保存"""
        filetuple = QFileDialog.getSaveFileName(self,
                'Save File', '', 'json (*.json)\nAll Files (*.*)')
        filename = filetuple[0]
        if len(filename)>0:
            self.__save(self.filename)
            self.__filename = filename
            self.setWindowTitle(u'PysideTestApplication [{0}]'.format(filename))

    def __save(self, filename):
        with codecs.open(filename,'w','utf-8') as f:
            f.write(json.dumps(self.treeModel.serialize(), indent=2, ensure_ascii=False))

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
