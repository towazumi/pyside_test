# coding: utf-8

from abc import ABCMeta, abstractmethod

class TreeItem(object):
    __metaclass__ = ABCMeta

    def __init__(self, parent = None):
        self.children = list()
        self.parent = parent
        if parent:
            parent.appendChild(self)

    def appendChild(self, item):
        if not isinstance(item, TreeItem):
            raise Exception('{} is not TreeItem'.format(type(item).__class__.__name__))
        self.children.append(item)

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0

    @abstractmethod
    def columnCount(self):
        pass

    @abstractmethod
    def headerData(self,column):
        pass

    @abstractmethod
    def data(self, column):
        pass
