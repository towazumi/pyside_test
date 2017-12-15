# coding:utf-8 

import os
import sys
import json

import logging
import logging.config

from Qt import QtGui, QtWidgets, QtCore

from log import SignalLogHandler
from widgets import SimpleOutputWidget

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

class TestWindow(QtWidgets.QMainWindow):
    """ テストウィンドウ """

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)

        # 出力ウィンドウ
        outputDock = QtWidgets.QDockWidget(u'出力ウィンドウ', self)
        outputWidget = SimpleOutputWidget(outputDock)
        outputDock.setWidget(outputWidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, outputDock)

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
    app = QtWidgets.QApplication(sys.argv)
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
