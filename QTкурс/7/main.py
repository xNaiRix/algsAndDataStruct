import sys


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QHBoxLayout, QPushButton, 
    QFrame, QColorDialog, QUndoView, QFileDialog,
    QMessageBox
)
from PySide6.QtGui import QAction, QKeySequence
from src.widgets.canvas import EditorCanvas
from src.widgets.properties import PropertiesPanel
from src.logic.strategies import JsonSaveStrategy, ImageSaveStrategy
from src.logic.factory import ShapeFactory
import json

class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vector Graphics Editor")
        self._setup_layout()
        self._init_ui()


    def _init_ui(self):
        self.statusBar().showMessage("Готов к работе")
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")#Амперсанд позволяет открывать меню через Alt+F

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Close the application")
        exit_action.triggered.connect(self.close) 
        file_menu.addAction(exit_action)

        save_action = QAction("Save as", self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip("Scene saved")
        save_action.triggered.connect(self.on_save_clicked)
        file_menu.addAction(save_action)

        open_action = QAction("Open file", self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip("Scene opened")
        open_action.triggered.connect(self.on_open_clicked)
        file_menu.addAction(open_action)
        
        toolbar = self.addToolBar("Main Toolbar")

        self.btn_line = QPushButton("Line")
        self.btn_rect = QPushButton("Rect")
        self.btn_ell = QPushButton("Ellipse")
        self.btn_hand= QPushButton("Hand")
        self.btn_line.setCheckable(True)
        self.btn_rect.setCheckable(True)
        self.btn_ell.setCheckable(True)
        self.btn_hand.setCheckable(True)


        self.btn_hand.setChecked(True)

        toolbar.addWidget(self.btn_line)
        toolbar.addWidget(self.btn_rect)
        toolbar.addWidget(self.btn_ell)
        toolbar.addWidget(self.btn_hand)
        
        self.btn_line.clicked.connect(lambda: self.on_change_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool("rect"))
        self.btn_ell.clicked.connect(lambda: self.on_change_tool("ellipse"))
        self.btn_hand.clicked.connect(lambda: self.on_change_tool("select"))
        self.current_tool = "select"

        toolbar.addSeparator()
        self.btn_clr = QPushButton("Color")
        self.btn_clr.setStyleSheet("background-color: #0f0f0f")
        toolbar.addWidget(self.btn_clr)
        self.btn_clr.clicked.connect(self.on_change_color)
        self.current_color = "black"
        self.canvas.set_color(self.current_color)
        self.canvas.set_tool(self.current_tool)

        
        group_action = QAction("Group", self)
        group_action.setShortcut(QKeySequence("Ctrl+G"))
        group_action.triggered.connect(self.canvas.group_selection)

        ungroup_action = QAction("Ungroup", self)
        ungroup_action.setShortcut(QKeySequence("Ctrl+U"))
        ungroup_action.triggered.connect(self.canvas.ungroup_selection)

        toolbar.addAction(group_action)
        toolbar.addAction(ungroup_action)


        self.props_panel = PropertiesPanel(self.canvas.scene, self.canvas.undo_stack)
        self.main_layout.addWidget(self.props_panel)


        stack = self.canvas.undo_stack
        undo_action = stack.createUndoAction(self, "&Undo")
        undo_action.setShortcut(QKeySequence.Undo)
        redo_action = stack.createRedoAction(self, "&Redo")
        redo_action.setShortcut(QKeySequence.Redo)

        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.canvas.delete_selected)
        self.menuBar().addAction(delete_action)
        self.addAction(delete_action)

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)


        self.undo_view = QUndoView(self.canvas.undo_stack)
        self.tools_layout.addWidget(self.undo_view)
        self.undo_view.show()
        


    def on_change_color(self):
        color = QColorDialog.getColor(self.current_color,self, "Выбери цвет")
        if not color.isValid():
            return
        self.current_color=color
        self.canvas.set_color(self.current_color)

    def on_change_tool(self, tool_name):
        self.current_tool = tool_name
        print(f"Выбран инструмент: {tool_name}")
        
        # Визуальная логика "Радио-кнопок"
        # Если выбрали Line, отжимаем Rect, и наоборот.
        # (В будущем заменим это на QActionGroup, но сейчас полезно написать руками)
        if tool_name == "line":
            self.btn_line.setChecked(True)
            self.btn_rect.setChecked(False)
            self.btn_ell.setChecked(False)
            self.btn_hand.setChecked(False)
        elif tool_name == "rect":
            self.btn_line.setChecked(False)
            self.btn_rect.setChecked(True)
            self.btn_ell.setChecked(False)
            self.btn_hand.setChecked(False)
        elif tool_name == "ellipse":
            self.btn_line.setChecked(False)
            self.btn_rect.setChecked(False)
            self.btn_ell.setChecked(True)
            self.btn_hand.setChecked(False)
        elif tool_name == "select":
            self.btn_line.setChecked(False)
            self.btn_rect.setChecked(False)
            self.btn_ell.setChecked(False)
            self.btn_hand.setChecked(True)
            

        self.canvas.set_tool(tool_name)

        
    def on_save_clicked(self):
        filters = "Vector Project (*.json);;PNG Image (*.png);;JPEG Image (*.jpg)"
        filename, selected_filter = QFileDialog.getSaveFileName(
            self, "Save File", "", filters
        )
        if not filename:
            return
        strategy = None
        if filename.lower().endswith(".png"):
            strategy = ImageSaveStrategy("PNG", background_color="transparent")
        elif filename.lower().endswith(".jpg"):
            strategy = ImageSaveStrategy("JPG", background_color="white") # JPG не умеет в прозрачность
        else:
            strategy = JsonSaveStrategy()

        try:
            strategy.save(filename, self.canvas.scene)
            self.statusBar().showMessage(f"Successfully saved to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}") 


    def on_open_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            "Открыть проект", 
            "", 
            "Vector Project (*.json *.vec)"
        )
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if "version" not in data or "shapes" not in data:
                raise ValueError("Некорректный формат файла")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось прочитать файл:\n{e}")
            return

        self.canvas.scene.clear()
        self.canvas.undo_stack.clear()
        
        scene_info = data.get("scene", {})
        width = scene_info.get("width", 800)
        height = scene_info.get("height", 600)
        self.canvas.scene.setSceneRect(0, 0, width, height)
        
        shapes_data = data.get("shapes", [])
        
        errors_count = 0
        
        for shape_dict in shapes_data:
            try:
                shape_obj = ShapeFactory.from_dict(shape_dict)
                print(shape_dict)
                self.canvas.scene.addItem(shape_obj)
            except Exception as e:
                print(f"Error loading shape: {e}")
                errors_count += 1
                
        if errors_count > 0:
            self.statusBar().showMessage(f"Загружено с ошибками ({errors_count} фигур пропущено)")
        else:
            self.statusBar().showMessage(f"Проект загружен: {path}")

    def _setup_layout(self):
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        tools_panel = QFrame()
        tools_panel.setFixedWidth(120)
        tools_panel.setStyleSheet("background-color: #000000")
        tools_layout = QVBoxLayout(tools_panel)


        self.canvas = EditorCanvas()
        self.tools_layout=tools_layout
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)
        self.main_layout = main_layout


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VectorEditorWindow()

    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()