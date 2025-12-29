from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QSpinBox, QPushButton,
                               QColorDialog, QHBoxLayout, QDoubleSpinBox)
from PySide6.QtCore import Qt, QPointF

from src.logic.commands import ChangeColorCommand, ChangeWidthCommand, MoveCommand

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtWidgets import  QGraphicsScene
    from PySide6.QtGui import QUndoStack 

    from src.logic.shapes import AbstractShape

class PropertiesPanel(QWidget):
    def __init__(self, scene:"QGraphicsScene", undo_stack:"QUndoStack"):
        super().__init__()
        self.scene:"QGraphicsScene"=scene
        self.undo_stack:"QUndoStack" = undo_stack

        self._init_ui()
        self.scene.selectionChanged.connect(self.on_selection_changed)
        self.spin_width.valueChanged.connect(self.on_width_changed)
        self.btn_color.clicked.connect(self.on_color_changed)
        self.spin_x.valueChanged.connect(self.on_geo_changed)
        self.spin_y.valueChanged.connect(self.on_geo_changed)

    def _init_ui(self)->None:
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #000000; border-left: 1px solid #ccc;")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Свойства")
        title.setStyleSheet("font-weight: bold; font-size: 14px;background-color:transparent")
        layout.addWidget(title)
        
        title_width = QLabel("Толщина обводки:")
        title_width.setStyleSheet("background-color: transparent;")
        layout.addWidget(title_width)
        self.spin_width:"QSpinBox" = QSpinBox()
        self.spin_width.setRange(1, 50)
        layout.addWidget(self.spin_width)

        title_color = QLabel("Цвет линии:")
        title_color.setStyleSheet("background-color: transparent;")
        layout.addWidget(title_color)
        self.btn_color:"QPushButton" = QPushButton()
        self.btn_color.setFixedHeight(30)
        layout.addWidget(self.btn_color)
        
        title_type = QLabel("Тип фигуры:")
        title_type.setStyleSheet("background-color: transparent;")
        layout.addWidget(title_type)
        self.lbl_type:"QLabel" = QLabel("Не выбрано")
        layout.addWidget(self.lbl_type)
        geo_layout = QHBoxLayout()

        self.spin_x:"QDoubleSpinBox" = QDoubleSpinBox()
        self.spin_x.setRange(-10000, 10000)
        self.spin_x.setPrefix("X: ")
        self.spin_x.valueChanged.connect(self.on_geo_changed)
        
        self.spin_y:"QDoubleSpinBox" = QDoubleSpinBox()
        self.spin_y.setRange(-10000, 10000)
        self.spin_y.setPrefix("Y: ")
        self.spin_y.valueChanged.connect(self.on_geo_changed)
        
        geo_layout.addWidget(self.spin_x)
        geo_layout.addWidget(self.spin_y)
        
        layout.addLayout(geo_layout)
        layout.addStretch()

        self.setEnabled(False)
    

    def on_selection_changed(self)->None:
        try:
            selected_items = self.scene.selectedItems()
        except RuntimeError as e:
            print("Error while selecting", e)
            return
        if not selected_items:
            self.setEnabled(False)
            self.spin_width.setValue(2)
            self.spin_width.setStyleSheet("background-color: #000000")
            self.btn_color.setStyleSheet("background-color: transparent")
            self.lbl_type.setText("Не выбрано")
            return
        
        self.setEnabled(True)
        self.update_width_ui(selected_items)
        self.update_color_ui(selected_items)
        item = selected_items[0]#костыль Из 5.1

        self.spin_x.blockSignals(True)
        self.spin_y.blockSignals(True)
        
        self.spin_x.setValue(item.x())
        self.spin_y.setValue(item.y())
        
        self.spin_x.blockSignals(False)
        self.spin_y.blockSignals(False)


        if hasattr(item, "type_name"):
            type_text = item.type_name.capitalize()
        else:
            type_text = type(item).__name__
        if len(selected_items) > 1:
            type_text += f" (+{len(selected_items)-1})"

        self.lbl_type.setText(type_text)


    def on_width_changed(self, value:int)->None:
        selected_items = self.scene.selectedItems()
        if not selected_items: return

        self.undo_stack.beginMacro("Change Width All")
        for item in selected_items:
            cmd = ChangeWidthCommand(item, value)
            self.undo_stack.push(cmd)
        self.undo_stack.endMacro()
            
        self.scene.update()

    def on_color_changed(self)->None:
        color = QColorDialog.getColor(title="Выберите цвет линии")
        if color.isValid():
            hex_color = color.name()
            self.btn_color.setStyleSheet(f"background-color: {hex_color}; border: 1px solid gray;")
            selected_items = self.scene.selectedItems()
            if not selected_items: return

            self.undo_stack.beginMacro("Change Color All")
            for item in selected_items:
                cmd = ChangeColorCommand(item, hex_color)
                self.undo_stack.push(cmd)
            self.undo_stack.endMacro()
        self.scene.update()


    def on_geo_changed(self, value)->None:
        selected_items = self.scene.selectedItems()
        if not selected_items: return
        self.undo_stack.beginMacro("Move items")
        for item in selected_items:
            new_x = self.spin_x.value()
            new_y = self.spin_y.value()
            cmd = MoveCommand(item, item.pos(), QPointF(new_x, new_y))
            self.undo_stack.push(cmd)
            #item.setPos(new_x, new_y)
        self.undo_stack.endMacro()
        
        self.scene.update()

    def update_width_ui(self, selected_items:list["AbstractShape"])->None:
        self.spin_width.blockSignals(True)
        first_width = 2
        is_mixed = False
        
        for i, item in enumerate(selected_items):
            if not hasattr(item, "current_width"): continue
            w = item.current_width
            if i == 0:
                first_width = w
            else:
                if w != first_width:
                    is_mixed = True
                    break
        if not first_width:
            first_width = 0
        if is_mixed or not first_width:
            self.spin_width.setValue(first_width)
            self.spin_width.setStyleSheet("background-color: #fffacd;")#LightYellow
            self.spin_width.setToolTip("Выбраны объекты с разной толщиной")
        else:
            self.spin_width.setValue(first_width)
            self.spin_width.setStyleSheet("background-color: #000000;")
            self.spin_width.setToolTip("")

        self.spin_width.blockSignals(False)

    def update_color_ui(self, selected_items:list["AbstractShape"])->None:
        self.btn_color.blockSignals(True)
        first_color = "black"
        is_mixed = False
        for i, item in enumerate(selected_items):
            if not hasattr(item, "current_color"): continue
            c = item.current_color
            if i == 0:
                first_color = c
            else:
                if c != first_color:
                    is_mixed = True
                    break
        if not first_color:
            first_color = "transparent"
        if is_mixed or first_color == "transparent":
            self.btn_color.setStyleSheet(f"background-color: {first_color}; border: 1px solid gray;")
            self.btn_color.setToolTip("Выбраны объекты с разным цветом")
        else:
            self.btn_color.setStyleSheet(f"background-color: {first_color}; border: 1px solid gray;")
            self.btn_color.setToolTip("")
        self.btn_color.blockSignals(False)
