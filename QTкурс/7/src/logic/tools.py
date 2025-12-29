from abc import ABC, abstractmethod
from PySide6.QtCore import Qt
from src.logic.factory import ShapeFactory
from src.logic.commands import AddShapeCommand, MoveCommand
from math import dist


class Tool(ABC):
    def __init__(self, view:"EditorCanvas"):
        self.view = view
        self.scene = view.scene

    @abstractmethod
    def mouse_press(self, event):
        pass

    @abstractmethod
    def mouse_move(self, event):
        pass

    @abstractmethod
    def mouse_release(self, event):
        pass


class SelectionTool(Tool):
    def __init__(self, view, undo_stack):
        super().__init__(view)
        self.undo_stack = undo_stack
        self.item_positions = {}

    def mouse_press(self, event):
        super(type(self.view), self.view).mousePressEvent(event)

        self.item_positions.clear()
        for item in self.scene.selectedItems():
            self.item_positions[item] = item.pos()

        
        if self.view.itemAt(event.pos()) and event.button() == Qt.LeftButton:
            self.view.setCursor(Qt.ClosedHandCursor)
        elif not self.view.itemAt(event.pos()):
            self.view.setCursor(Qt.ArrowCursor)



    def mouse_move(self, event):
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

    
    def mouse_release(self, event):
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
    def __init__(self, view, shape_type: str, undo_stack:AddShapeCommand, color: str = "black"):
        super().__init__(view)
        self.shape_type = shape_type
        self.color = color
        self.undo_stack = undo_stack

        self.start_pos = None
        self.temp_shape = None

    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = self.view.mapToScene(event.pos())
            try:
                self.create_shape(self.start_pos)
            except ValueError as e:
                print("ValueError:", e)
            except Exception as e:
                print("Error:", e)

        #super(type(self.view), self.view).mousePressEvent(event)

    def mouse_move(self, event):
        if self.temp_shape and self.start_pos:
            current_pos = self.view.mapToScene(event.pos())
            self.temp_shape.set_geometry(self.start_pos, current_pos)
        #super(type(self.view), self.view).mouseMoveEvent(event)

    def mouse_release(self, event):
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
            self.start_pos = None
 
    def create_shape(self, end_pos):
        self.temp_shape = ShapeFactory.create_shape(
                    self.shape_type,
                    self.start_pos,
                    end_pos,
                    self.color,
                    2
                )
        self.scene.addItem(self.temp_shape)

    def delete_shape(self):
        if self.temp_shape:
            self.scene.removeItem(self.temp_shape)
            self.temp_shape = None
    def set_color(self, color):
        self.color = color
