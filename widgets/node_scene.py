# coding:utf-8 

from PySide.QtCore import *
from PySide.QtGui import *

from node_base import EdgePoint, Edge

class NodeScene(QGraphicsScene):

    def __init__(self, parent=None):
        QGraphicsScene.__init__(self,parent)

        self.editing_edge = None

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(),QTransform())

        if isinstance(item, EdgePoint):
            edge = Edge()
            edge.setEdgePoint(item)
            edge.setMousePos(event.scenePos())

            self.addItem(edge)
            self.editing_edge = edge
        else:
            QGraphicsScene.mousePressEvent(self,event)


    def mouseMoveEvent(self,event):
        if self.editing_edge:
            self.editing_edge.setMousePos(event.scenePos())            
        else:
            QGraphicsScene.mousePressEvent(self,event)


    def mouseReleaseEvent(self,event):
        if self.editing_edge:
            item = self.itemAt(event.scenePos(),QTransform())
            if isinstance(item, EdgePoint):
                self.editing_edge.setEdgePoint(item)
            if not self.editing_edge.connected():
                self.editing_edge.reset()
                self.removeItem(self.editing_edge)
            self.editing_edge = None
        else:
            QGraphicsScene.mouseReleaseEvent(self,event)

