from PySide6.QtCore import Qt

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.logic.factory import ShapeFactory
from src.logic.commands import AddShapeCommand, MoveCommand
from src.config import DEFAULT_STROKE_WIDTH, DEFAULT_COLOR, ShapeName

if TYPE_CHECKING:
    from PySide6.QtWidgets import QGraphicsScene
    from PySide6.QtGui import QUndoStack, QMouseEvent
    from PySide6.QtCore import QPointF
    
    from src.widgets.canvas import EditorCanvas
    from src.logic.shapes import Shape



class Tool(ABC):
    def __init__(self, view:"EditorCanvas"):
        self.view: "EditorCanvas" = view
        self.scene: "QGraphicsScene" = view.scene

    @abstractmethod
    def mouse_press(self, event:"QMouseEvent")->None:
        pass

    @abstractmethod
    def mouse_move(self, event:"QMouseEvent")->None:
        pass

    @abstractmethod
    def mouse_release(self, event:"QMouseEvent")->None:
        pass


class SelectionTool(Tool):
    def __init__(self, view:"EditorCanvas", undo_stack:"QUndoStack"):
        super().__init__(view)
        self.undo_stack:"QUndoStack" = undo_stack
        self.item_positions:dict = {}

    def mouse_press(self, event:"QMouseEvent")->None:
        super(type(self.view), self.view).mousePressEvent(event)

        self.item_positions.clear()
        for item in self.scene.selectedItems():
            self.item_positions[item] = item.pos()

        if self.view.itemAt(event.pos()) and event.button() == Qt.LeftButton:
            self.view.setCursor(Qt.ClosedHandCursor)
        elif not self.view.itemAt(event.pos()):
            self.view.setCursor(Qt.ArrowCursor)

    def mouse_move(self, event:"QMouseEvent")->None:
        super(type(self.view), self.view).mouseMoveEvent(event)
        item = self.view.itemAt(event.pos())
        if event.buttons() & Qt.LeftButton:
            if item:
                self.view.setCursor(Qt.ClosedHandCursor)
            else:
                self.view.setCursor(Qt.ArrowCursor)
        else:
            if item:
                self.view.setCursor(Qt.OpenHandCursor)
            else:
                self.view.setCursor(Qt.ArrowCursor)

    def mouse_release(self, event:"QMouseEvent")->None:
        super(type(self.view), self.view).mouseReleaseEvent(event)  
        moved_items = []
        for item, old_pos in self.item_positions.items():
            new_pos = item.pos()
            if new_pos != old_pos:
                moved_items.append((item, old_pos, new_pos))
        
        if moved_items:
            self.undo_stack.beginMacro("Move Items")
            for item, old_pos, new_pos in moved_items:
                cmd = MoveCommand(item, old_pos, new_pos)
                self.undo_stack.push(cmd)
                
            self.undo_stack.endMacro()
        self.item_positions.clear()

        item = self.view.itemAt(event.pos())
        if item:
            self.view.setCursor(Qt.OpenHandCursor)
        else:
            self.view.setCursor(Qt.ArrowCursor)

        
class CreationTool(Tool):
    def __init__(self,
                 view:"EditorCanvas",
                 shape_type: ShapeName,
                 undo_stack:"QUndoStack",
                 color: str = DEFAULT_COLOR
                ):
        super().__init__(view)
        self.shape_type:str = shape_type
        self.color:str = color
        self.undo_stack:"QUndoStack" = undo_stack

        self.start_pos:"QPointF"|None = None
        self.temp_shape: "Shape"|None  = None

    def mouse_press(self, event:"QMouseEvent")->None:
        if event.button() == Qt.LeftButton:
            self.start_pos = self.view.mapToScene(event.pos())
            try:
                self.create_shape(self.start_pos)
            except ValueError as e:
                print("ValueError:", e)
            except Exception as e:
                print("Error:", e)

        #super(type(self.view), self.view).mousePressEvent(event)

    def mouse_move(self, event:"QMouseEvent")->None:
        if self.temp_shape and self.start_pos:
            current_pos = self.view.mapToScene(event.pos())
            self.temp_shape.set_geometry(self.start_pos, current_pos)
        #super(type(self.view), self.view).mouseMoveEvent(event)

    def mouse_release(self, event:"QMouseEvent")->None:
        if self.start_pos and event.button() == Qt.LeftButton:
            print(f"Tool {self.shape_type}: Фигура добавлена")
            current_pos = self.view.mapToScene(event.pos())
            
            self.delete_shape()
            try:
                final_shape = ShapeFactory.create_shape(self.shape_type, self.start_pos, current_pos, color="black")
                command = AddShapeCommand(self.scene, final_shape)
                self.undo_stack.push(command)
                print(f"Command pushed: {command.text()}")
            except ValueError as e:
                    pass
            self.start_pos:"QPointF"|None = None
 
    def create_shape(self, end_pos:"QPointF"):
        self.temp_shape = ShapeFactory.create_shape(
                    self.shape_type,
                    self.start_pos,
                    end_pos,
                    self.color,
                    DEFAULT_STROKE_WIDTH
                )
        self.scene.addItem(self.temp_shape)

    def delete_shape(self)->None:
        if self.temp_shape:
            self.scene.removeItem(self.temp_shape)
            self.temp_shape = None

    def set_color(self, color:str)->None:
        self.color = color
