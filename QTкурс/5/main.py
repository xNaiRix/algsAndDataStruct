import sys


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QVBoxLayout, QHBoxLayout, QPushButton, 
    QFrame, QColorDialog
)
from PySide6.QtGui import QAction, QKeySequence
from src.widgets.canvas import EditorCanvas
from src.widgets.properties import PropertiesPanel

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

        self.current_color = "black"
        self.canvas.set_color(self.current_color)
        self.canvas.set_tool(self.current_tool)

        #Группировка
        group_action = QAction("Group", self)
        group_action.setShortcut(QKeySequence("Ctrl+G"))
        group_action.triggered.connect(self.canvas.group_selection)

        ungroup_action = QAction("Ungroup", self)
        ungroup_action.setShortcut(QKeySequence("Ctrl+U"))
        ungroup_action.triggered.connect(self.canvas.ungroup_selection)

        toolbar.addAction(group_action)
        toolbar.addAction(ungroup_action)


        self.props_panel = PropertiesPanel(self.canvas.scene)
        self.main_layout.addWidget(self.props_panel)
        


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

        
    def _setup_layout(self):
        container = QWidget()
        self.setCentralWidget(container)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        tools_panel = QFrame()
        tools_panel.setFixedWidth(120)
        tools_panel.setStyleSheet("background-color: #000000")
        tools_layout = QVBoxLayout(tools_panel)
        self.btn_clr = QPushButton("Color")
        tools_layout.addWidget(self.btn_clr)
        self.btn_clr.clicked.connect(self.on_change_color)
        tools_layout.addStretch()


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