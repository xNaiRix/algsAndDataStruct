import sys

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt

from logic import Solver, Sector
from typing import Literal, Callable

class InputSectorsLayout(QWidget):
    KNOWNMODE= 0
    UNKNOWNMODE= 1
    def __init__(self, radio_button:QRadioButton, sect_name:str, f:Callable):
        super().__init__()

        self.layout:QHBoxLayout = QHBoxLayout(self)
        self.radiobutton:QRadioButton = radio_button
        self.sect_name:str = sect_name
        self.layout.addWidget(self.radiobutton)
        self.name_lb = QLabel(self.sect_name)
        self.name_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_lb.setStyleSheet("background-color: transparent")
        self.layout.addWidget(self.name_lb, stretch=2)
        self.layout.addStretch(1)

        #known
        self.open_lb = QLabel("[")
        self.open_lb.setStyleSheet("background-color: transparent")
        self.leftBorder_lnedt = QLineEdit()
        self.sep_lb = QLabel(";")
        self.sep_lb.setStyleSheet("background-color: transparent")
        self.rightBorder_lnedt = QLineEdit()
        self.close_lb = QLabel("]")
        self.close_lb.setStyleSheet("background-color: transparent")

        self.layout.addWidget(self.open_lb, stretch=1)
        self.open_lb.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.leftBorder_lnedt, stretch=2)
        self.layout.addWidget(self.sep_lb, stretch=0)
        self.layout.addWidget(self.rightBorder_lnedt, stretch=2)
        self.layout.addWidget(self.close_lb, stretch=1)
        self.close_lb.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #Unknown
        self.find_btn = QPushButton("Найти")
        self.layout.addWidget(self.find_btn, stretch=5)
        #self.find_btn.setMinimumWidth(800)
        self.find_btn.hide()
        self.find_btn.clicked.connect(lambda : f(self))
        self.mode = self.KNOWNMODE

    def switchMode(self)->Literal[0, 1]:
        if self.mode == self.KNOWNMODE:
            self.mode = self.UNKNOWNMODE
        elif self.mode == self.UNKNOWNMODE:
            self.mode = self.KNOWNMODE
        self.setMode(self.mode)
        return self.mode

    def setMode(self, mode:Literal[0, 1])->None:
        self.mode = mode
        if mode == InputSectorsLayout.KNOWNMODE:
            self.find_btn.hide()

            self.open_lb.show()
            self.leftBorder_lnedt.show()
            self.sep_lb.show()
            self.rightBorder_lnedt.show()
            self.close_lb.show()

        elif mode == InputSectorsLayout.UNKNOWNMODE:
            self.find_btn.show()
            
            self.open_lb.hide()
            self.leftBorder_lnedt.hide()
            self.sep_lb.hide()
            self.rightBorder_lnedt.hide()
            self.close_lb.hide()
        else:
            print("Incorrect mode")

    def getMode(self)->Literal[0,1]:return self.mode
    def getName(self)->str: return self.sect_name
    def getSect(self)->Sector:
        if self.mode == self.UNKNOWNMODE: raise ValueError("Ну не знаю я какой, там отрезок, не вводили его!!")
        try:
            l = float(self.leftBorder_lnedt.text())
            r = float(self.rightBorder_lnedt.text())
        except Exception as e:
            print(e)
            raise ValueError("Incorrect input")
        return Sector([l, r])
    
    def __repr__(self):
        return f"mode:{self.mode} name:{ self.sect_name}"
    

class Solver15Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.solver:Solver = Solver()
        self.setWindowTitle("Task 15 solver")
        self._setup_layout()

        self.isKnown_groupBtn:QButtonGroup = QButtonGroup()
        self._connect_buttons()

        self.sector_widgets:dict[int, InputSectorsLayout] = {}#id кнопки: виджет
    
    def _setup_layout(self):
        container = QWidget()
        self.setCentralWidget(container)
        self.main_layout = QVBoxLayout(container)
        self.inputExp_layout = QVBoxLayout()
        self.inputSectors_layout = QVBoxLayout()
        self.answer_layout = QHBoxLayout()
        self.main_layout.addLayout(self.inputExp_layout)
        self.main_layout.addLayout(self.inputSectors_layout)
        self.main_layout.addLayout(self.answer_layout)
        self.main_layout.addStretch()

        self._setup_inputExp_layout()
        self._setup_inputSectors_layout()
        self._setup_answer_layout()


    def _setup_inputExp_layout(self):
        self.inputExp_layout.addWidget(QLabel("Введите логическое выражение"))
        input_layout = QHBoxLayout()
        self.inputExp_layout.addLayout(input_layout)
        self.exp_lnedt = QLineEdit()
        input_layout.addWidget(self.exp_lnedt)
        self.initExp_btn = QPushButton()
        self.initExp_btn.setText("Установить выражение")
        input_layout.addWidget(self.initExp_btn)


    def _setup_inputSectors_layout(self):
        self.inputSectors_layout.addWidget(QLabel("Введите известные отрезки"))

    def _setup_answer_layout(self):
        sector_layout = QVBoxLayout()
        len_layout = QVBoxLayout()
        cnt_layout = QVBoxLayout()
        self.answer_layout.addLayout(sector_layout)
        self.answer_layout.addLayout(len_layout)
        self.answer_layout.addLayout(cnt_layout)

        sector_layout.addWidget(QLabel("Искомый отрезок"))
        len_layout.addWidget(QLabel("Длина искомого отрезка"))
        cnt_layout.addWidget(QLabel("Количество целых точек в искомом отрезке"))

        self.sect_lnedt = QLineEdit()
        self.len_lnedt = QLineEdit()
        self.cnt_lnedt = QLineEdit()
        for lnedt in [self.sect_lnedt, self.len_lnedt, self.cnt_lnedt]:
            lnedt.setReadOnly(True)
        
        sector_layout.addWidget(self.sect_lnedt)
        len_layout.addWidget(self.len_lnedt)
        cnt_layout.addWidget(self.cnt_lnedt)
        
    def _connect_buttons(self):
        self.initExp_btn.clicked.connect(self._on_initExp_click)
        self.exp_lnedt.returnPressed.connect(self.initExp_btn.click)
        self.isKnown_groupBtn.idClicked.connect(lambda btn_id: self._on_changeMode_click(btn_id))

    def _on_initExp_click(self):
        exp = self.exp_lnedt.text()
        print(exp)
        try:
            self.solver.setExp(exp)
            print(self.solver.exp)
        except Exception as e:
            print("some error with setting exp:", e)
            return
        try:
            buttons = self.isKnown_groupBtn.buttons()
            for button in buttons:
                self.isKnown_groupBtn.removeButton(button)
                button.setParent(None)
                button.deleteLater()
            for widget in self.sector_widgets.values():
                self.inputSectors_layout.removeWidget(widget)
                widget.setParent(None)
                widget.deleteLater()

            self.sector_widgets.clear()

            sect_names = self.solver.getSectorNames()
            for i, name in enumerate(sect_names):
                self.sector_widgets[i] =  InputSectorsLayout(QRadioButton(), name, self._on_solve_click)
                self.inputSectors_layout.addWidget(self.sector_widgets[i])
                self.isKnown_groupBtn.addButton(self.sector_widgets[i].radiobutton, i)
                self.sector_widgets[i].setMode(InputSectorsLayout.KNOWNMODE)

        except Exception as e:
            print("some error in setting sector widgets:", e)

    def _on_changeMode_click(self, btn_id:int):
        print("id", btn_id)
        for widget in self.sector_widgets.values():
            if widget.getMode() == InputSectorsLayout.UNKNOWNMODE:
                widget.switchMode()
        self.sector_widgets[btn_id].switchMode()
    

    def _on_solve_click(self, sector:InputSectorsLayout):
        sector_variables = {}
        for widget in self.sector_widgets.values():
            if widget.getMode() == InputSectorsLayout.KNOWNMODE:
                sector_variables[widget.getName()] = widget.getSect()

        ans:Sector = self.solver.solve(sector_variables)
        self.sect_lnedt.setReadOnly(False)
        self.sect_lnedt.setText(str(ans))
        self.sect_lnedt.setReadOnly(True)

        self.len_lnedt.setReadOnly(False)
        self.len_lnedt.setText(str(ans.size()))
        self.len_lnedt.setReadOnly(True)

        self.cnt_lnedt.setReadOnly(False)
        self.cnt_lnedt.setText(str(ans.cnt()))
        self.cnt_lnedt.setReadOnly(True)
 
def main():
    app = QApplication(sys.argv)
    
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

    """)
    window = Solver15Window()

    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()