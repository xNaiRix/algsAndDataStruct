from PySide6.QtCore import QPointF

from src.logic.shapes import Rectangle, Line, Ellipse, Group, Shape, AbstractShape
from src.config import (TYPE_RECT, TYPE_LINE, TYPE_ELLIPSE, TYPE_GROUP, ShapeName,
                        DEFAULT_STROKE_WIDTH, DEFAULT_COLOR)
from typing import get_args

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: ShapeName,
                     start_point:QPointF,
                     end_point:QPointF,
                     color: str|None=None,
                     width:int|None=None
                     )->Shape:
        
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()
        if shape_type == TYPE_LINE:
            return Line(x1, y1, x2, y2, color, width)
            
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        if shape_type == TYPE_RECT:
            return Rectangle(x,y,w,h,color,width)
        elif shape_type == TYPE_ELLIPSE:
            return Ellipse(x,y,w,h,color,width)
        else:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
        
    @staticmethod
    def from_dict(data:dict)->AbstractShape:
        shape_type = data.get("type")
        if shape_type == TYPE_GROUP:
            return ShapeFactory._create_group(data)
        elif shape_type in get_args(ShapeName):
            return ShapeFactory._create_primitive(data)
        else:
            raise ValueError(f"Unknown type: {shape_type}")
        
    @staticmethod
    def _create_primitive(data:dict)->Shape:
        props = data.get("props", {})
        shape_type = data.get("type")

        color = props.get("color", DEFAULT_COLOR)
        stroke_width = props.get("stroke_width", DEFAULT_STROKE_WIDTH)

        if shape_type == TYPE_RECT:
            obj = Rectangle(props["x"], props["y"], props["w"], props["h"], color, stroke_width)
        elif shape_type == TYPE_ELLIPSE:
            obj = Ellipse(props["x"], props["y"], props["w"], props["h"], color, stroke_width)
        elif shape_type == TYPE_LINE:
            obj = Line(props['x1'], props['y1'], props['x2'], props['y2'], color, stroke_width)
        
        if "pos" in data:
            obj.setPos(data["pos"][0], data["pos"][1])

        return obj
    

    @staticmethod
    def _create_group(data:dict)->Group:
        group = Group()
        x,y = data.get("pos", [0,0])
        group.setPos(x,y)
        children_data = data.get("children", [])
        for child_dict in children_data:
            child_item = ShapeFactory.from_dict(child_dict)
            group.addToGroup(child_item)
            if "pos" in child_dict:
                cx, cy = child_dict["pos"]
                child_item.setPos(cx, cy)
        return group

    