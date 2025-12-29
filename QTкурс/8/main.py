import sys
import json

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
from src.config import ToolName, DEFAULT_SCENE_WIDTH, DEFAULT_SCENE_HEIGHT,DEFAULT_COLOR
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtWidgets import QToolBar

class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vector Graphics Editor")
        self._setup_layout()
        self._init_ui()


    def _init_ui(self)->None:
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
        self._setup_tool_buttons(toolbar)
        toolbar.addSeparator()
        color_action = QAction("Color", self)
        color_action.setShortcut("Ctrl+U")
        color_action.triggered.connect(self.on_change_color)
        self.current_color:str = DEFAULT_COLOR
        self.canvas.set_color(self.current_color)
        
        group_action = QAction("Group", self)
        group_action.setShortcut(QKeySequence("Ctrl+G"))
        group_action.triggered.connect(self.canvas.group_selection)

        ungroup_action = QAction("Ungroup", self)
        ungroup_action.setShortcut(QKeySequence("Ctrl+U"))
        ungroup_action.triggered.connect(self.canvas.ungroup_selection)

        toolbar.addAction(color_action)
        toolbar.addAction(group_action)
        toolbar.addAction(ungroup_action)


        self.props_panel:"PropertiesPanel" = PropertiesPanel(self.canvas.scene, self.canvas.undo_stack)
        self.main_layout.addWidget(self.props_panel)


        stack = self.canvas.undo_stack
        undo_action = stack.createUndoAction(self, "&Undo")
        undo_action.setShortcut(QKeySequence.Undo)
        redo_action = stack.createRedoAction(self, "&Redo")
        redo_action.setShortcut(QKeySequence.Redo)

        delete_action = QAction("Delete", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.canvas.delete_selected)

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addAction(delete_action)


        self.undo_view:"QUndoView" = QUndoView(self.canvas.undo_stack)
        self.tools_layout.addWidget(self.undo_view)
        self.undo_view.show()
        


    def _setup_tool_buttons(self, toolbar:"QToolBar")->None:
        self.tool_buttons:dict["ToolName", "QPushButton"] = {
            'line': QPushButton("Line"),
            'rect': QPushButton("Rect"),
            'ellipse': QPushButton("Ellipse"),
            'select': QPushButton("Hand")
        }
        for tool_name, button in self.tool_buttons.items():
            button.setCheckable(True)
            button.clicked.connect(lambda checked=False, tn=tool_name: self.on_change_tool(tn))
            toolbar.addWidget(button)
        
        self.tool_buttons['select'].setChecked(True)
        self.current_tool: "ToolName" = 'select'
        self.canvas.set_tool('select')
        #print([[n, b.text()] for n, b in self.tool_buttons.items()])



    def on_change_color(self)->None:
        color = QColorDialog.getColor(self.current_color,self, "Выбери цвет")
        if not color.isValid():
            return
        self.current_color=color.name()
        self.canvas.set_color(self.current_color)



    def on_change_tool(self, tool_name:ToolName)->None:
        if tool_name == self.current_tool:
            return
        self.current_tool:"ToolName" = tool_name
        print(f"Выбран инструмент: {tool_name}")
        
        for button in self.tool_buttons.values():
            button.setChecked(False)
        self.tool_buttons[tool_name].setChecked(True)
        self.canvas.set_tool(tool_name)

        

    def on_save_clicked(self)->None:
        filters = "Vector Project (*.vec);;Vector Project (*.json);;PNG Image (*.png);;JPEG Image (*.jpg)"
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



    def on_open_clicked(self)->None:
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
        width = scene_info.get("width", DEFAULT_SCENE_WIDTH)
        height = scene_info.get("height", DEFAULT_SCENE_HEIGHT)
        self.canvas.scene.setSceneRect(0, 0, width, height)
        
        shapes_data = data.get("shapes", [])
        
        errors_count = 0
        self.canvas.scene.blockSignals(True)
        for shape_dict in shapes_data:
            try:
                shape_obj = ShapeFactory.from_dict(shape_dict)
                #print(shape_dict)
                self.canvas.scene.addItem(shape_obj)
            except Exception as e:
                print(f"Error loading shape: {e}")
                errors_count += 1
                
        if errors_count > 0:
            self.statusBar().showMessage(f"Загружено с ошибками ({errors_count} фигур пропущено)")
        else:
            self.statusBar().showMessage(f"Проект загружен: {path}")
        self.canvas.scene.blockSignals(False)
        self.canvas.scene.update()
        


    def _setup_layout(self)->None:
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        tools_panel = QFrame()
        tools_panel.setFixedWidth(120)
        tools_panel.setStyleSheet("background-color: #000000")
        tools_layout = QVBoxLayout(tools_panel)


        self.canvas:"EditorCanvas" = EditorCanvas()
        self.tools_layout:"QVBoxLayout"=tools_layout
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)
        self.main_layout:"QHBoxLayout" = main_layout





def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Глобальный CSS стиль для всего приложения
    app.setStyleSheet("""
        QWidget {
            color: #ffffff;
            background-color: #2b2b2b;
        }
        
        QPushButton {
            background-color: #3c3c3c;
            border: 1px solid #555555;
            border-radius: 3px;
            padding: 5px;
            color: #ffffff;
        }
        
        QPushButton:hover {
            background-color: #4a4a4a;
            border: 1px solid #666666;
        }
        
        QPushButton:checked {
            background-color: #1e6fb8;
            border: 1px solid #2a82da;
        }
        
        QPushButton:pressed {
            background-color: #155a8a;
        }
        
        QFrame {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QUndoView {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #555555;
        }
        
        QToolBar {
            background-color: #2b2b2b;
            border: none;
            spacing: 3px;
        }
        
        QMenuBar {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QMenuBar::item:selected {
            background-color: #3c3c3c;
        }
        
        QMenu {
            background-color: #2b2b2b;
            color: #ffffff;
            border: 1px solid #555555;
        }
        
        QMenu::item:selected {
            background-color: #1e6fb8;
        }
        
        QStatusBar {
            background-color: #2b2b2b;
            color: #ffffff;
        }
    """)
    window = VectorEditorWindow()

    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()