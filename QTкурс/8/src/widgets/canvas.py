from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QUndoStack
from src.logic.tools import SelectionTool, CreationTool
from src.logic.shapes import Group
from src.logic.commands import DeleteShapeCommand
from src.config import (TOOL_RECT, TOOL_LINE, TOOL_SELECT, TOOL_ELLIPSE, ToolName,
                         TYPE_ELLIPSE, TYPE_RECT, TYPE_LINE,
                         DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT, BG_COLOR, UNDO_LIMIT
                         )
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtCore import QEvent
    from src.logic.tools import Tool


class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.scene:"QGraphicsScene" = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT) 
        self.setRenderHint(self.renderHints() | QPainter.Antialiasing)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"background-color: {BG_COLOR}")

        self.undo_stack:"QUndoStack" = QUndoStack(self)
        self.undo_stack.setUndoLimit(UNDO_LIMIT)

        self.tools:dict[str, "Tool"] = {
            TOOL_SELECT:SelectionTool(self, self.undo_stack),
            TOOL_RECT:CreationTool(self, TYPE_RECT, self.undo_stack),
            TOOL_LINE:CreationTool(self, TYPE_LINE, self.undo_stack),
            TOOL_ELLIPSE:CreationTool(self, TYPE_ELLIPSE, self.undo_stack)
        }
        self.active_tool = self.tools[TOOL_SELECT]



    def set_tool(self, tool_name:ToolName)->None:
        if tool_name in self.tools:
            self.active_tool:"Tool" = self.tools[tool_name]
            print(f"Инструмент переключен на: {tool_name}")
            if tool_name == TOOL_SELECT:
                self.setCursor(Qt.ArrowCursor)
            else:
                self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event:"QEvent")->None:
        try:
            print(self.active_tool.shape_type)
        except Exception:
            pass
        self.active_tool.mouse_press(event)
    
    def mouseMoveEvent(self, event:"QEvent")->None:
        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event:"QEvent")->None:
        try:
            print(self.active_tool.shape_type)
        except Exception:
            pass
        self.active_tool.mouse_release(event)


    def group_selection(self)->None:
        selected_items = self.scene.selectedItems()
        if not selected_items:
            return
        group = Group()
        self.scene.addItem(group)
        for item in selected_items:
            item.setSelected(False)
            group.addToGroup(item)
        group.setSelected(True)
        

    def ungroup_selection(self)->None:
        selected_items = self.scene.selectedItems()

        for item in selected_items:
            if isinstance(item, Group):
                self.scene.destroyItemGroup(item)

    def set_color(self, color:str)->None:
        for tool in self.tools.values():
            if isinstance(tool, CreationTool):
                tool.set_color(color)
            

    def delete_selected(self)->None:
        selected = self.scene.selectedItems()
        if not selected:
            return
        self.undo_stack.beginMacro("Delete Selection")
        for item in selected:
            cmd = DeleteShapeCommand(self.scene, item)
            self.undo_stack.push(cmd)
        self.undo_stack.endMacro()
            