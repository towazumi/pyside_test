# coding:utf-8

from PySide.QtCore import *
from PySide.QtGui import *
from treeitem import TreeItem

class TreeItemRoot(TreeItem):
    
    def __init__(self):
        TreeItem.__init__(self)

    def columnCount(self):
        if len(self.children)==0:
            return 0
        return self.child(0).columnCount()

    def headerData(self,column):
        if len(self.children)==0:
            return 0
        return self.child(0).headerData(column)

    def data(self, column):
        return None

class TreeModel(QAbstractItemModel):
    
    def __init__(self, parent=None):
        QAbstractItemModel.__init__(self,parent)
        self.root = TreeItemRoot()

    def rowCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().childCount()
        return self.root.childCount()

    def columnCount(self, parent):
        parentItem = parent.internalPointer() if parent.isValid() else self.root
        return parentItem.columnCount()

    def headerData(self, column, orientation, role):
        if role != Qt.DisplayRole:
            return QAbstractItemModel.headerData(self, column, orientation, role)
        if orientation==Qt.Horizontal:
            if column < self.root.columnCount():
                return self.root.headerData(column)
        return None

    def data(self, index, role):
        if not index.isValid():
            return None
        if role != Qt.DisplayRole:
            return None
        return index.internalPointer().data(index.column())

    def index(self, row, column, parent):
        parentItem = parent.internalPointer() if parent.isValid() else self.root
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row,column,childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        if not childItem:
            return QModelIndex()
        parentItem = childItem.parent
        if parentItem == self.root:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

