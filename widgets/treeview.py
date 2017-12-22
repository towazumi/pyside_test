# coding: utf-8

from PySide.QtGui import *
import logging

class TreeView(QTreeView):

    def __init__(self, parent=None):
        QTreeView.__init__(self,parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        # self.dragDropOverwriteMode()
        # self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.logger = logging.getLogger()

    def dragEnterEvent(self,event):
        self.logger.debug('dragEnterEvent')
        QTreeView.dragEnterEvent(self,event)
        event.accept()

    def dragMoveEvent(self,event):
        self.logger.debug('dragMoveEvent')
        QTreeView.dragMoveEvent(self,event)
        
        event.accept()

    def dropEvent(self,event):
        self.logger.debug('dropEvent')
        QTreeView.dropEvent(self,event)

