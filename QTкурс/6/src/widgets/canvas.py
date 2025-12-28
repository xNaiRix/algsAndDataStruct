from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QUndoStack
from src.logic.factory import ShapeFactory
from src.logic.tools import SelectionTool, CreationTool
from src.logic.shapes import Group
from src.logic.commands import DeleteShapeCommand
class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600) 
        self.setRenderHint(self.renderHints() | QPainter.Antialiasing)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #ffffff")

        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(50)

        self.tools = {
            "select":SelectionTool(self, self.undo_stack),
            "rect":CreationTool(self, "rect", self.undo_stack),
            "line":CreationTool(self, "line", self.undo_stack),
            "ellipse":CreationTool(self, "ellipse", self.undo_stack)
        }
        self.active_tool = self.tools["select"]



    def set_tool(self, tool_name):
        if tool_name in self.tools:
            self.active_tool = self.tools[tool_name]
            print(f"Инструмент переключен на: {tool_name}")
            if tool_name == "select":
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event):
        try:
            print(self.active_tool.shape_type)
        except Exception:
            pass
        self.active_tool.mouse_press(event)
    
    def mouseMoveEvent(self, event):
        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        try:
            print(self.active_tool.shape_type)
        except Exception:
            pass
        self.active_tool.mouse_release(event)


    def group_selection(self):
        selected_items = self.scene.selectedItems()
        if not selected_items:
            return
        group = Group()
        self.scene.addItem(group)
        for item in selected_items:
            item.setSelected(False)
            group.addToGroup(item)
        group.setSelected(True)
        

    def ungroup_selection(self):
        selected_items = self.scene.selectedItems()

        for item in selected_items:
            if isinstance(item, Group):
                self.scene.destroyItemGroup(item)

    def set_color(self, color):
        for tool in self.tools.values():
            if isinstance(tool, CreationTool):
                tool.set_color(color)

    def delete_selected(self):
        selected = self.scene.selectedItems()
        if not selected:
            return

        self.undo_stack.beginMacro("Delete Selection")
        
        for item in selected:
            cmd = DeleteShapeCommand(self.scene, item)
            self.undo_stack.push(cmd)
            
        self.undo_stack.endMacro()
            