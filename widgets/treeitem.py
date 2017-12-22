# coding: utf-8

from abc import ABCMeta, abstractmethod
import copy

class IDGenerator:
    def __init__(self):
        self.id = 0

    def next(self):
        self.id += 1
        return self.id

class TreeItem(object):
    __metaclass__ = ABCMeta

    id_generator = IDGenerator()
    def __init__(self, parent = None):
        self.internal_id = TreeItem.id_generator.next()
        self.children = list()
        self.parent = parent
        if parent:
            parent.appendChild(self)
        

    def appendChild(self, item):
        if not isinstance(item, TreeItem):
            raise Exception('{} is not TreeItem'.format(type(item).__class__.__name__))
        
        # 親があれば親の子から除外 
        if item.parent is not None and item in item.parent.children:
            item.parent.children.remove(item)

        # 接続 
        item.parent = self
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
    def editable(self, column):
        return False

    @abstractmethod
    def data(self, column):
        pass

    @abstractmethod
    def setData(self, column, value):
        return False

    def serialize(self):
        d = dict()
        d['__class__'] = self.__class__.__name__
        for k, v in vars(self).items():
            if k in ('parent', 'children', 'internal_id'):
                continue
            if hasattr(v,"serialize"):
                d[k] = v.serialize()
            else:
                d[k] = v 

        if len(self.children):
            d['children'] = list()
            for c in self.children:
                d['children'].append(c.serialize())
        return d

    def deserialize(self, data, proto_types):
        for k, v in data.items():
            if k=='children':
                for child in v:
                    classname = child['__class__']
                    print(classname)
                    obj = copy.deepcopy(proto_types[classname])
                    obj.deserialize(child,proto_types)
                    self.appendChild(obj)
                continue
            if k in ('__class__',):
                continue
            value = getattr(self,k)
            if hasattr(value,"deserialize"):
                value.deserialize(v,proto_types)
                setattr(self,k,value)
            else:
                print(k,v)
                setattr(self,k,v)



        
