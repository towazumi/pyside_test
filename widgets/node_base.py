# coding:utf-8

from PySide.QtCore import *
from PySide.QtGui import *
import enum

class EdgePointType(enum.Enum):
    IN = 0
    OUT = 1
    UNDEFINED = 2


class EdgePoint(QGraphicsItem):

    def __init__(self, parent=None, scene=None):
        QGraphicsItem.__init__(self, parent, scene)
        self.type = EdgePointType.UNDEFINED
        self.size = QSizeF(4.0,4.0)
        self.connected_edges = list()

    def boundingRect(self):
        margin = 2.0
        rect = self.contentRect()
        rect.setWidth(2.0*margin+rect.width())
        rect.setHeight(2.0*margin+rect.height())
        rect.translate(-margin,-margin)
        return rect
    
    def contentRect(self):
        return QRectF(QPointF(0.0,0.0), self.size)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(255,255,255))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QColor(100,100,100))
        painter.drawEllipse(QPointF(0.0,0.0),self.size.width(), self.size.height())

class Edge(QGraphicsItem):

    def __init__(self,parent=None,scene=None):
        QGraphicsItem.__init__(self,parent,scene)
        self.setZValue(1)

        self.input_edge = None
        self.output_edge = None
        
        # つながってない時用 
        self.mousePos = QPointF(0.0,0.0)

    def boundingRect(self):
        pos1, pos2 = self.posTuple()
        return QRectF( pos1, QSizeF(pos2.x()-pos1.x(), pos2.y()-pos1.y()) ).normalized()

    def reset(self):
        if self.input_edge:
            self.input_edge.connected_edges.remove(self)

        if self.output_edge:
            self.output_edge.connected_edges.remove(self)

    def setMousePos(self,pos):
        self.prepareGeometryChange()
        self.mousePos = pos


    def posTuple(self):
        if self.connected():
            return ( self.input_edge.scenePos(), self.output_edge.scenePos() )

        if self.input_edge:
            return ( self.input_edge.scenePos(), self.mousePos )
        
        if self.output_edge:
            return ( self.output_edge.scenePos(), self.mousePos )

        return ( self.mousePos, self.mousePos )

    def connected(self):
        return self.input_edge is not None and self.output_edge is not None

    def setEdgePoint(self, edgePoint):
        if edgePoint.type == EdgePointType.IN:
            if self.input_edge:
                return

            self.input_edge = edgePoint
            self.input_edge.connected_edges.append(self)

        elif edgePoint.type == EdgePointType.OUT:
            if self.output_edge:
                return

            self.output_edge = edgePoint
            self.output_edge.connected_edges.append(self)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(255,255,255))
        pen.setWidth(2)
        painter.setPen(pen)
        pos1, pos2 = self.posTuple()
        painter.drawLine(pos1, pos2)


class NodeBase(QGraphicsItem):

    def __init__(self, parent=None, scene=None):
        QGraphicsItem.__init__(self, parent, scene)
        self.name = self.__class__.__name__
        self.size = QSizeF(100.0,50.0)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self.input_attributes = list()
        self.output_attributes = list()

    def setupEdgePoints(self):

        content_rect = QRectF( QPointF(0.0, 10.0), QSizeF(self.size.width(), self.size.height()-10.0 ))

        for i in xrange(0, len(self.input_attributes)):

            attribute =  self.input_attributes[i]

            x = content_rect.left() 
            y = content_rect.top() + (i+1) * (content_rect.size().height() / (len(self.input_attributes)+1.0))

            edge_point = EdgePoint(self)
            edge_point.type =  EdgePointType.IN
            edge_point.setPos( QPointF(x,y) )

            setattr(self,attribute,edge_point)


        for i in xrange(0, len(self.output_attributes)):

            attribute =  self.output_attributes[i]

            x = content_rect.right() 
            y = content_rect.top() + (i+1) * (content_rect.size().height() / (len(self.output_attributes)+1.0))

            edge_point = EdgePoint(self)
            edge_point.type =  EdgePointType.OUT
            edge_point.setPos( QPointF(x,y) )

            setattr(self,attribute,edge_point)

    def boundingRect(self):
        margin = 4.0
        rect = self.contentRect()
        rect.setWidth(2.0*margin+rect.width())
        rect.setHeight(2.0*margin+rect.height())
        rect.translate(-margin,-margin)
        return rect

    def contentRect(self):
        return QRectF(QPointF(0.0,0.0), self.size)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(255,255,255))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QColor(100,100,100))
        painter.drawRoundedRect(self.contentRect(), 5, 5)

        font = painter.font()
        font.setBold(True)
        painter.setFont(font)

        text_rect = self.contentRect()
        text_rect.setBottom(20.0)
        painter.drawText(text_rect, Qt.AlignCenter, self.name)

        content_rect = self.contentRect()
        content_rect.setTop(content_rect.top() + 10.0)

        # input text 
        for i in xrange(0, len(self.input_attributes)):
            attribute =  self.input_attributes[i]
            edge_point = getattr(self,attribute)
            text_rect = QRectF(edge_point.pos(), QSizeF(100.0, 20.0))
            text_rect.translate(10.0, -10.0)
            painter.drawText( text_rect, Qt.AlignLeft | Qt.AlignVCenter, attribute )

        # output text 
        for i in xrange(0, len(self.output_attributes)):
            attribute =  self.output_attributes[i]
            edge_point = getattr(self,attribute)
            text_rect = QRectF(edge_point.pos(), QSizeF(100.0, 20.0))
            text_rect.translate(-110.0, -10.0)
            painter.drawText( text_rect, Qt.AlignRight | Qt.AlignVCenter, attribute )

    def mousePressEvent(self, event):
        QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        # つながってるラインの更新
        for attribute in (self.input_attributes + self.output_attributes):
            edgePoint = getattr(self, attribute)
            for edge in edgePoint.connected_edges:
                edge.prepareGeometryChange()

        QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        QGraphicsItem.mouseReleaseEvent(self, event)





