from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from factory import ShapeFactory
from tools import SelectionTool, CreationTool

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


        self.tools = {
            "select":SelectionTool(self),
            "rect":CreationTool(self, "rect"),
            "line":CreationTool(self, "line"),
            "ellipse":CreationTool(self, "ellipse")
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

    def set_color(self, color):
        for tool in self.tools.values():
            if isinstance(tool, CreationTool):
                tool.set_color(color)