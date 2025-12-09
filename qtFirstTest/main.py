import myui
from PySide6 import QtWidgets
import sys

class Application(QtWidgets.QMainWindow, myui.Ui_Dialog ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sumButton.clicked.connect(lambda : self.operation("+"))
        self.multyButton.clicked.connect(lambda : self.operation("*"))
        self.differenceButton.clicked.connect(lambda : self.operation("-"))
        self.divButton.clicked.connect(lambda : self.operation("/"))
        self.intDivButton.clicked.connect(lambda : self.operation("//", True))
        self.remButton.clicked.connect(lambda : self.operation("%", True))


    def operation(self, op, isInt = False):
        x = self.FirstNumber.text()
        y = self.SecondNumber.text()
        try:
            if isInt:
                result = eval("int(x)" +op+ "int(y)")
            else:
                result = eval("float(x)" +op+ "float(y)")
            self.result.setText(str(result))
        except Exception as e:
            self.result.setText(e)

app = QtWidgets.QApplication(sys.argv)
main_window = Application()
main_window.show()
app.exec()