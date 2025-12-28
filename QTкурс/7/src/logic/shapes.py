from abc import ABC, ABCMeta, abstractmethod
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup
from PySide6.QtGui import QPen, QColor, QPainterPath
from PySide6.QtCore import QPointF, Qt


class AbstractShape(ABC):
    @property
    @abstractmethod
    def type_name(self) -> str:
        #'rect', 'line', 'ellipse'
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        #{'type': 'rect', 'x': 10, 'y': 20, ...}
        pass
    @abstractmethod
    def set_geometry(self,start_point:QPointF, end_point:QPointF):
        pass
class ShapeMeta(type(QGraphicsPathItem), ABCMeta):
    pass

class Shape(QGraphicsPathItem, AbstractShape, metaclass=ShapeMeta):
    def __init__(self, color: str|None = "black", stroke_width: int|None = 2):
        super().__init__()
        self.current_color = color
        self.current_width = stroke_width
        
        self._setup_pen()
        self._setup_flags()

    def _setup_pen(self):
        pen = QPen(QColor(self.current_color))
        pen.setWidth(self.current_width)
        self.setPen(pen)

    def _setup_flags(self):
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable, True)


    def set_active_color(self, color: str):
        self.current_color = color
        self._setup_pen()

    def set_stroke_width(self, width: int):
        self.current_width = width
        self._setup_pen()



class Rectangle(Shape):
    def __init__(self,x,y,w,h,color="black", stroke_width=2):
        if color is None:
            color = "black"
        if stroke_width is None:
            stroke_width = 2
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
            "pos": [self.x(), self.y()],
            "props": {
                "x": self.x0, "y": self.y0, 
                "w": self.w, "h": self.h,
                "color": self.current_color,
                "stroke_width": self.current_width
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
        if color is None:
            color = "black"
        if stroke_width is None:
            stroke_width = 2

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
            "pos": [self.x(), self.y()],
            "props": {
                "x1": self.x1, "y1": self.y1, 
                "x2": self.x2, "y2": self.y2,
                "color": self.current_color,
                "stroke_width": self.current_width
            }
        }
    
    def set_geometry(self, start_point, end_point):
        self.x1, self.y1 =start_point.x(), start_point.y()
        self.x2, self.y2 = end_point.x(), end_point.y()

        self._create_geometry()
    
class Ellipse(Shape):
    def __init__(self, x,y,w,h,color="black", stroke_width=2):
        if color is None:
            color = "black"
        if stroke_width is None:
            stroke_width = 2

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
            "pos": [self.x(), self.y()],
            "props": {
                "x": self.x0, "y": self.y0, 
                "w": self.w, "h": self.h,
                "color": self.current_color,
                "stroke_width": self.current_width
            }
        }
    
    def set_geometry(self, start_point, end_point):
        self.x0 = min(start_point.x(), end_point.x())
        self.y0 = min(start_point.y(), end_point.y())
        self.w = abs(end_point.x() - start_point.x())
        self.h = abs(end_point.y() - start_point.y())

        self._create_geometry()
        #print("geometry_set")

class GroupMeta(type(QGraphicsItemGroup), ABCMeta):
    pass

class Group(QGraphicsItemGroup, AbstractShape, metaclass=GroupMeta):
    def __init__(self):
        super().__init__()

        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
        self.setHandlesChildEvents(True)

        self.current_color = "black"
        self.current_width = 2

    def addToGroup(self, item):
        children = self.childItems()
        new_width = None
        if hasattr(item, "current_width") :
            new_width = item.current_width
        elif hasattr(item, "pen") and item.pen() is not None:
            new_width = item.pen().width()

        if len(children) == 0:
            if new_width is not None:
                self.current_width = new_width
            return super().addToGroup(item)
        

        if self.current_width != new_width:
            self.current_width = None#считаем, что так, если Mixed
        print("current w", self.current_width)
        return super().addToGroup(item)        

    @property
    def type_name(self)->str:
        return "group"
    
    def set_geometry(self,start_point:QPointF, end_point:QPointF):
        pass

    def set_active_color(self, color:str):
        self.current_color = color
        for child in self.childItems():
            if isinstance(child, Shape):
                child.set_active_color(color)

    def set_stroke_width(self, width: int):
        self.current_width = width
        for child in self.childItems():
            if isinstance(child, Shape):
                child.set_stroke_width(width)

    def to_dict(self)->dict:
        children_data = []
        for child in self.childItems():
            if isinstance(child, Shape):
                children_data.append(child.to_dict())
        return {
            "type":self.type_name,
            "x":self.pos().x(),
            "y":self.pos().y(),
            "children": children_data
        }

