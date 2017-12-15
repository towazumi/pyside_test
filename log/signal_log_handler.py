# coding:utf-8 

from logging import Handler
from Qt.QtCore import Signal,QObject

class SignalWrapper(QObject):
    """ SignalLogHandlerに渡すためのSignalのラッパー """
    signal = Signal(str)
    def __init__(self, *args, **kwargs):
        super(SignalWrapper,self).__init__(*args, **kwargs)

    def send_log(self, string):
        self.signal.emit(string)

class SignalLogHandler(Handler):
    """ PySideのSignalを利用するログハンドラ """

    # ログ送り先
    signal = SignalWrapper()

    def __init__(self, *args, **kwargs):
        super(SignalLogHandler,self).__init__(*args, **kwargs)

    def emit(self,record):
        formatted = self.format(record)
        self.signal.send_log(formatted)
    
    @staticmethod
    def connect(slot):
        SignalLogHandler.signal.signal.connect(slot)


