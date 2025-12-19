from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from factory import ShapeFactory

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600) 
        self.setRenderHint(self.renderHints() | QPainter.Antialiasing)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #ffffff")

        self.active_tool = "line" 
        self.active_color = "black"
        self.start_point = None



    def set_tool(self, tool_name):
        self.active_tool = tool_name

    def mousePressEvent(self, event):
        print(self.active_tool)
        if event.button() == Qt.LeftButton and self.active_tool!="hand":
            self.start_point=self.scene_pos = self.mapToScene(event.pos())
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        #отпускаем ЛКМ
        print(self.active_tool)
        if self.start_point and event.button() == Qt.LeftButton and self.active_tool!="hand":
            end_point = self.mapToScene(event.pos())
            try:
                new_shape = ShapeFactory.create_shape(
                    self.active_tool,
                    self.start_point,
                    end_point,
                    self.active_color
                )
                self.scene.addItem(new_shape)
                print(f"Created shape: {self.active_tool}")
            except ValueError:
                pass
            finally:
                self.start_point = None
        super().mouseReleaseEvent(event)

    def set_color(self, color):
        self.active_color = color