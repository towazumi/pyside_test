# coding:utf-8

import logging
import json
import copy
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

    def editable(self, column):
        return False

    def data(self, column):
        return None

    def setData(self, column, value):
        return False

    def serialize(self):
        d = list()
        for c in self.children:
            d.append(c.serialize())
        return d

class TreeModel(QAbstractItemModel):
    
    def __init__(self, parent=None):
        QAbstractItemModel.__init__(self,parent)
        self.logger = logging.getLogger()
        self.root = TreeItemRoot()
        self.mimeType = 'custom_data'

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
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        return index.internalPointer().data(index.column())

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        elif role != Qt.EditRole:
            return False

        index.internalPointer().setData(index.column(),value)
        return True

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

    def insertColumns(self, position, columns, parent=QModelIndex()):
        return True

    def insertRows(self, position, rows, parent=QModelIndex()):
        return success

    def flags(self, index):
        flags = QAbstractTableModel.flags(self, index)
        if index.isValid():
            if index.internalPointer().editable(index.column()):
                flags |= Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled | Qt.ItemIsEditable
        return flags

    def mimeTypes(self):
        return [self.mimeType]

    def mimeData(self, indices):
        self.logger.debug('call mimeData len:{}'.format(len(indices)))
        itemset = set()
        for index in indices:
            itemset.add(index.internalPointer().internal_id)
        mime = QMimeData()
        mime.setData(self.mimeType, QByteArray(json.dumps(list(itemset))))
        return mime

    def dropMimeData(self, data, action, row, column, parent):
        self.logger.debug('dropMimeData %s %s %s %s' % (data.data(self.mimeType), action, row, parent) )
        return True

    def supportedDropActions(self): 
        self.logger.debug('call supportedDropActions')
        return Qt.CopyAction | Qt.MoveAction

    def serialize(self):
        """ データをpython辞書形式に変換 """
        return self.root.serialize()

    def deserialize(self, data_list, proto_types):
        """ python辞書形式のデータの読み込み """
        # ルートを作り直す 
        self.beginResetModel()
        self.root = TreeItemRoot()

        for data in data_list:
            classname = data['__class__']
            obj = copy.deepcopy(proto_types[classname])
            obj.deserialize(data,proto_types)
            self.root.appendChild(obj)

        self.endResetModel()
        




