from PySide6.QtGui import QUndoCommand
from src.logic.shapes import Group, AbstractShape
from src.config import DEFAULT_STROKE_WIDTH, DEFAULT_COLOR
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtWidgets import QGraphicsScene
    from PySide6.QtCore import QPointF


class AddShapeCommand(QUndoCommand):
    def __init__(self, scene:"QGraphicsScene", item:"AbstractShape"):
        super().__init__()
        self.scene:"QGraphicsScene" = scene
        self.item:"AbstractShape" = item
        name = "Shape"
        if hasattr(item, "type_name"):
            name = item.type_name
        self.setText(f"Add {name}")

    def redo(self)->None:
        if self.item.scene() != self.scene:
            self.scene.addItem(self.item)

    def undo(self)->None:
        self.scene.removeItem(self.item)


class DeleteShapeCommand(QUndoCommand):
    def __init__(self, scene:"QGraphicsScene", item:"AbstractShape"):
        super().__init__()
        self.scene:"QGraphicsScene" = scene
        self.item:"AbstractShape" = item
        self.setText(f"Delete {item.type_name}")

    def redo(self)->None:
        self.scene.removeItem(self.item)

    def undo(self)->None:
        self.scene.addItem(self.item)


class MoveCommand(QUndoCommand):
    def __init__(self, item:"AbstractShape", old_pos:"QPointF", new_pos:"QPointF"):
        super().__init__()
        self.item:"AbstractShape" = item
        self.old_pos:"QPointF" = old_pos
        self.new_pos:"QPointF" = new_pos
        self.setText(f"Move {item.type_name}")

    def undo(self)->None:
        self.item.setPos(self.old_pos)

    def redo(self)->None:
        self.item.setPos(self.new_pos)

class ChangeColorCommand(QUndoCommand):
    def __init__(self, item:"AbstractShape", new_color:str):
        super().__init__()
        self.item:"AbstractShape" = item
        self.new_color:str = new_color
        self.old_color:dict = self._save_color(item)#{item: {color:, children:[]}}
        self.setText(f"Change Color to {new_color}")

    def redo(self)->None:
        if hasattr(self.item, "set_active_color"):
            self.item.set_active_color(self.new_color)

    def undo(self)->None:
        self._set_old_color(self.old_color)


    def _save_color(self, item:"AbstractShape")->dict:
        old_color=  {"item":item, "color": self._get_color(item), "children": []}
        if isinstance(item, Group):
            for child in item.childItems():
                old_color["children"].append(self._save_color(child))
        return old_color
    
    def _set_old_color(self, old_color:dict)->None:
        if old_color["color"] is not None:
            if hasattr(old_color["item"], "set_active_color"):
                old_color["item"].set_active_color(old_color["color"])
            return
        for child in old_color["children"]:
            self._set_old_color(child)

    def _get_color(self, item:"AbstractShape")->str|None:
        if hasattr(item, "current_color"):
            return item.current_color
        elif hasattr(item, "pen") and item.pen() is not None:
            return item.pen().color().name()
        return DEFAULT_COLOR


class ChangeWidthCommand(QUndoCommand):
    def __init__(self, item:"AbstractShape", new_width:int):
        super().__init__()
        self.item:"AbstractShape" = item
        self.new_width:int = new_width
        self.old_width:dict = self._save_width(item)#{item: {width:, children:[]}}
        self.setText(f"Change Width to {new_width}")

    def redo(self)->None:
        if hasattr(self.item, "set_stroke_width"):
            self.item.set_stroke_width(self.new_width)

    def undo(self)->None:
        self._set_old_width(self.old_width)

    def _save_width(self, item:"AbstractShape")->dict:
        old_width=  {"item":item, "width": self._get_width(item), "children": []}
        if isinstance(item, Group):
            for child in item.childItems():
                old_width["children"].append(self._save_width(child))
        return old_width
    
    def _set_old_width(self, old_width:dict)->None:
        if old_width["width"] is not None:
            if hasattr(old_width["item"], "set_stroke_width"):
                old_width["item"].set_stroke_width(old_width["width"])
            return
        for child in old_width["children"]:
            self._set_old_width(child)


    def _get_width(self, item:"AbstractShape")->int|None:
        if hasattr(item, "current_width"):
            return item.current_width
        elif hasattr(item, "pen"):
            return item.pen().width()
        return DEFAULT_STROKE_WIDTH
        
