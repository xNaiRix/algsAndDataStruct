from abc import ABC, ABCMeta, abstractmethod
from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup
from PySide6.QtGui import QPen, QColor, QPainterPath

from src.config import (TYPE_RECT, TYPE_LINE, TYPE_ELLIPSE, TYPE_GROUP,
                         FigureName, DEFAULT_STROKE_WIDTH, DEFAULT_COLOR)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtCore import QPointF

class AbstractShape(ABC):
    @property
    @abstractmethod
    def type_name(self) -> FigureName:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        #{'type': 'rect', 'x': 10, 'y': 20, ...}
        pass
    @abstractmethod
    def set_geometry(self,start_point:"QPointF", end_point:"QPointF"):
        pass


class ShapeMeta(type(QGraphicsPathItem), ABCMeta):
    pass

class Shape(QGraphicsPathItem, AbstractShape, metaclass=ShapeMeta):
    def __init__(self, color: str|None = DEFAULT_COLOR, stroke_width: int|None = DEFAULT_STROKE_WIDTH):
        super().__init__()

        if color is None:
            color = DEFAULT_COLOR
        if stroke_width is None:
            stroke_width = DEFAULT_STROKE_WIDTH

        self.current_color:str = color
        self.current_width:int = stroke_width
        
        self._setup_pen()
        self._setup_flags()

    def _setup_pen(self)->None:
        pen = QPen(QColor(self.current_color))
        pen.setWidth(self.current_width)
        self.setPen(pen)

    def _setup_flags(self)->None:
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable, True)


    def set_active_color(self, color: str)->None:
        self.current_color:str = color
        self._setup_pen()

    def set_stroke_width(self, width: int)->None:
        self.current_width:int = width
        self._setup_pen()

    def in_group(self)->bool:
        parent = self.parentItem()
        return parent is not None and isinstance(parent, QGraphicsItemGroup)

class Rectangle(Shape):
    def __init__(self,
                 x:float,
                 y:float,
                 w:float,
                 h:float,
                 color:str|None=DEFAULT_COLOR,
                 stroke_width:int|None=DEFAULT_STROKE_WIDTH):
        
        super().__init__(color=color, stroke_width=stroke_width)
        self.x0:float=x
        self.y0:float=y
        self.w:float=w
        self.h:float=h
        self._create_geometry()

    def _create_geometry(self)->None:
        path = QPainterPath()
        path.addRect(self.x0, self.y0, self.w,self.h)
        self.setPath(path)

    @property
    def type_name(self)->FigureName:
        return TYPE_RECT
    
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
    
    def set_geometry(self, start_point:"QPointF", end_point:"QPointF")->None:
        self.x0:float = min(start_point.x(), end_point.x())
        self.y0:float = min(start_point.y(), end_point.y())
        self.w:float = abs(end_point.x() - start_point.x())
        self.h:float = abs(end_point.y() - start_point.y())

        self._create_geometry()

class Line(Shape):
    def __init__(self,
                 x1:float,
                 y1:float,
                 x2:float,
                 y2:float,
                 color:str|None=DEFAULT_COLOR,
                 stroke_width:int|None=DEFAULT_STROKE_WIDTH):
        super().__init__(color, stroke_width)
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

        self._create_geometry()

    def _create_geometry(self)->None:
        path = QPainterPath()
        path.moveTo(self.x1, self.y1)
        path.lineTo(self.x2,self.y2)

        self.setPath(path)

    @property
    def type_name(self)->FigureName:
        return TYPE_LINE
    
    def to_dict(self)->dict:
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
    
    def set_geometry(self, start_point:"QPointF", end_point:"QPointF")->None:
        self.x1:float = start_point.x()
        self.y1:float = start_point.y()
        self.x2:float = end_point.x()
        self.y2:float = end_point.y()

        self._create_geometry()
    
class Ellipse(Shape):
    def __init__(self,
                 x:float,
                 y:float,
                 w:float,
                 h:float,
                 color:str|None=DEFAULT_COLOR,
                 stroke_width:int|None=DEFAULT_STROKE_WIDTH):
        super().__init__(color=color, stroke_width=stroke_width)
        self.x0:float=x
        self.y0:float=y
        self.w:float=w
        self.h:float=h
        self._create_geometry()

    def _create_geometry(self)->None:
        path = QPainterPath()
        path.addEllipse(self.x0, self.y0, self.w, self.h)
        self.setPath(path)

    @property
    def type_name(self)->FigureName:
        return TYPE_ELLIPSE
    
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
    
    def set_geometry(self, start_point:"QPointF", end_point:"QPointF")->None:
        self.x0:float = min(start_point.x(), end_point.x())
        self.y0:float = min(start_point.y(), end_point.y())
        self.w:float = abs(end_point.x() - start_point.x())
        self.h:float = abs(end_point.y() - start_point.y())

        self._create_geometry()

class GroupMeta(type(QGraphicsItemGroup), ABCMeta):
    pass

class Group(QGraphicsItemGroup, AbstractShape, metaclass=GroupMeta):
    def __init__(self):
        super().__init__()

        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
        self.setHandlesChildEvents(True)

        self.current_color = DEFAULT_COLOR
        self.current_width = DEFAULT_STROKE_WIDTH

    def addToGroup(self, item:"AbstractShape")->None:
        children = self.childItems()
        new_width = None
        new_color = None
        if hasattr(item, "current_width") :
            new_width = item.current_width
        elif hasattr(item, "pen") and item.pen() is not None:
            new_width = item.pen().width()

        if hasattr(item, "current_color") :
            new_color = item.current_color
        elif hasattr(item, "pen") and item.pen() is not None:
            new_color = item.pen().color().name()

        if len(children) == 0:
            if new_width is not None:
                self.current_width:int|None = new_width
                self.current_color:str|None = new_color
            return super().addToGroup(item)
        

        if self.current_width != new_width:
            self.current_width:int|None = None#считаем, что так, если Mixed
        
        if self.current_color != new_color:
            self.current_color:str|None = None
        return super().addToGroup(item)        

    @property
    def type_name(self)->FigureName:
        return TYPE_GROUP
    
    def set_geometry(self,start_point:"QPointF", end_point:"QPointF"):
        pass

    def set_active_color(self, color:str):
        self.current_color:str|None = color
        for child in self.childItems():
            try:
                child.set_active_color(color)
            except Exception: continue

    def set_stroke_width(self, width: int):
        self.current_width:int|None = width
        for child in self.childItems():
            try:
                child.set_stroke_width(width)
            except Exception: continue

    def to_dict(self)->dict:
        children_data = []
        for child in self.childItems():
            try:
                children_data.append(child.to_dict())
            except Exception: continue

        return {
            "type":self.type_name,
            "x":self.pos().x(),
            "y":self.pos().y(),
            "children": children_data
        }

    def in_group(self)->bool:
        parent = self.parentItem()
        return parent is not None and isinstance(parent, QGraphicsItemGroup)

