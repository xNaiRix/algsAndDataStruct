from abc import ABC, ABCMeta, abstractmethod
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPen, QColor, QPainterPath
from PySide6.QtCore import QPointF

class ShapeMeta(type(QGraphicsPathItem), ABCMeta):
    pass

class Shape(QGraphicsPathItem, metaclass=ShapeMeta):
    def __init__(self, color: str = "black", stroke_width: int = 2):
        super().__init__()
        self.color = color
        self.stroke_width = stroke_width
        
        self._setup_pen()
        self._setup_flags()

    def _setup_pen(self):
        pen = QPen(QColor(self.color))
        pen.setWidth(self.stroke_width)
        self.setPen(pen)

    def _setup_flags(self):
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable, True)

    @property
    @abstractmethod
    def type_name(self) -> str:
        #'rect', 'line', 'ellipse'
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        #{'type': 'rect', 'x': 10, 'y': 20, ...}
        pass

    def set_active_color(self, color: str):
        self.color = color
        self._setup_pen()

    @abstractmethod
    def set_geometry(self,start_point:QPointF, end_point:QPointF):
        pass


class Rectangle(Shape):
    def __init__(self,x,y,w,h,color="black", stroke_width=2):
        super().__init__(color=color, stroke_width=stroke_width)
        self.x0=x
        self.y0=y
        self.w=w
        self.h=h
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        #print("create geometry rect")
        path.addRect(self.x0, self.y0, self.w,self.h)
        self.setPath(path)

    @property
    def type_name(self)->str:
        return "rect"
    
    def to_dict(self)->dict:
        return {
            "type": self.type_name,
            "props": {
                "x": self.x0, "y": self.y0, 
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }
    
    def set_geometry(self, start_point, end_point):
        self.x0 = min(start_point.x(), end_point.x())
        self.y0 = min(start_point.y(), end_point.y())
        self.w = abs(end_point.x() - start_point.x())
        self.h = abs(end_point.y() - start_point.y())

        self._create_geometry()

class Line(Shape):
    def __init__(self,x1,y1, x2,y2, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.moveTo(self.x1, self.y1)
        path.lineTo(self.x2,self.y2)

        self.setPath(path)

    @property
    def type_name(self):
        return "line"
    
    def to_dict(self):
        return {
            "type": self.type_name,
            "props": {
                "x1": self.x1, "y1": self.y1, 
                "x2": self.x2, "y2": self.y2,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }
    
    def set_geometry(self, start_point, end_point):
        self.x1, self.y1 =start_point.x(), start_point.y()
        self.x2, self.y2 = end_point.x(), end_point.y()

        self._create_geometry()
    
class Ellipse(Shape):
    def __init__(self, x,y,w,h,color="black", stroke_width=2):
        super().__init__(color=color, stroke_width=stroke_width)
        self.x0=x
        self.y0=y
        self.w=w
        self.h=h
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.addEllipse(self.x0, self.y0, self.w, self.h)
        self.setPath(path)

    @property
    def type_name(self)->str:
        return "ellipse"
    
    def to_dict(self):
        return {
            "type": self.type_name,
            "props": {
                "x1": self.x0, "y1": self.y0, 
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }
    
    def set_geometry(self, start_point, end_point):
        self.x0 = min(start_point.x(), end_point.x())
        self.y0 = min(start_point.y(), end_point.y())
        self.w = abs(end_point.x() - start_point.x())
        self.h = abs(end_point.y() - start_point.y())

        self._create_geometry()
        #print("geometry_set")
