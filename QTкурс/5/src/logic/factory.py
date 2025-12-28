from src.logic.shapes import Rectangle, Line, Ellipse, Group
from PySide6.QtCore import QPointF
class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str, start_point:QPointF, end_point:QPointF, color: str|None=None,width:int|None=None):
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()
        if shape_type == 'line':
            return Line(x1, y1, x2, y2, color, width)
            
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        if shape_type == 'rect':
            return Rectangle(x,y,w,h,color,width)
        elif shape_type == 'ellipse':
            return Ellipse(x,y,w,h,color,width)
        else:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
        
    @staticmethod
    def from_dict(data:dict):
        shape_type = data.get("type")

        if shape_type == "group":
            return ShapeFactory._create_group(data)
        elif shape_type in ["rect", "line", "ellipse"]:
            return ShapeFactory._create_primitive(data)
        else:
            raise ValueError(f"Unknown type: {shape_type}")
        
    @staticmethod
    def _create_primitive(data:dict):
        props = data.get("props", {})
        shape_type = data.get("type")

        color = props.get("color", "black")
        stroke_width = props.get("stroke_width", 2)

        if shape_type == "rect":
            obj = Rectangle(props["x"], props["y"], props["w"], props["h"], color, stroke_width)
        elif shape_type == "ellips":
            obj = Ellipse(props["x"], props["y"], props["w"], props["h"], color, stroke_width)
        elif shape_type == "line":
            obj = Line(props['x1'], props['y1'], props['x2'], props['y2'], color, stroke_width)
        
        if "pos" in data:
            obj.setPos(data["pos"][0], data["pos"][1])

        return obj
    

    @staticmethod
    def _create_group(data:dict):
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

    