from shapes import Rectangle, Line, Ellipse
from PySide6.QtCore import QPointF
class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str, start_point:QPointF, end_point:QPointF, color: str|None=None,width:int|None=None):
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()
        # Для линий нам нужны именно точки начала и конца (даже если тянем назад)
        if shape_type == 'line':
            if color and width: 
                return Line(x1, y1, x2, y2, color, width)
            if not color and not width:
                return Line(x1, y1, x2, y2)
            if not width:
                return Line(x1, y1, x2, y2, color=color)
            if not width:
                return Line(x1, y1, x2, y2, stroke_width=width)
            
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        #print(x,y,w,h)
        args = {}
        for name, val in zip(["x", "y", "w", "h", "color", "stroke_width"], [x,y,w,h, color, width]):
            if val or val == 0:
                args[name]=val

        if shape_type == 'rect':
            #print(args)
            return Rectangle(**args)
        elif shape_type == 'ellipse':
            return Ellipse(**args)
        else:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")