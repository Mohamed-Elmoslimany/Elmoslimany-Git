import sys
from threading import Thread
import time
from typing import Any
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTabWidget, QCheckBox, QComboBox,
    QRadioButton, QGroupBox, QButtonGroup, QSpinBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt


flag = True

class MainWindow(QMainWindow):

    def __init__(self, *args, GUI_type = None, **kwargs):
        super().__init__()
        self.setWindowTitle('Trace GUI')
        self.show()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.hbox1 = QHBoxLayout(central_widget)
        self.hbox2 = QHBoxLayout(central_widget)
        self.vbox = QVBoxLayout(central_widget)

        print(args, kwargs)

        self.GUI_type = GUI_type
        self.args = kwargs.keys()
        print(f"\n{kwargs = }\n{self.args = }\n")
        self.general_trace = []
        # self.flag = True

        # for arg in args:
            # label = QLabel(f"{arg= }", self)
            # obj = Tracer(arg, arg, label)
            # self.general_trace.append(label)
            # self.general_trace.append(QLabel(f"{obj.name= }, {obj.value= }", self))

        # for k, v in kwargs.items():
            # obj = Prepare(k, v)
            # self.general_trace.append(QLabel(f"{obj.name= }, {obj.value= }", self))

        self.setStyleSheet("QLabel{border: 2px solid black; border-radius: 5px; margin: 5px;}"
                           "QHBoxLayout{border: 2px solid black; border-radius: 5px; margin: 5px;}"
                           "QVBoxLayout{border: 2px solid black; border-radius: 5px; margin: 5px;}")
        self.trace(*args, **kwargs)
        # self.initUI()
        Thread(target=self.update, args=kwargs, daemon=True).start()

    def initUI(self):
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        for label in self.general_trace:
            self.hbox1.addWidget(label)

    def on_button_click(self):
        pass

    def update(self, *args):
        # print(*self.glbl.items(), sep = ", ")
        # for v in self.args:
            # print(f"{v}: ")
        print()
        print(f"{args = }\n{list(self.glbl.keys()) = }\n")
        # for v, k in list(self.glbl.items()):
            # print(f"{v}: {k}")
        while flag:
            # print(self.args)
            # print(label2)
            # for i, arg in enumerate(self.args):
                # self.general_trace[i].setText(f"{arg= }")
            time.sleep(1)
            for arg in args:
                print(self.glbl[arg])

    def trace(self, *args, **kwargs):
        self.glbl = globals()
        self.args = args
        for arg in args:
            self.glbl[arg] = arg
        for k, v in kwargs.items():
            self.glbl[k] = v

    def closeEvent(self, event):
        global flag
        flag = False
        event.accept()


class Tracer():
    def __init__(self, name, value, parent = "general"):
        self.name = name
        self.value = value
        self.parent = parent

    def __setattr__(self, name: str, value: Any) -> None:
        pass


def main(*args, **kwargs):
    global window1
    app = QApplication(sys.argv)
    window1 = MainWindow(*args, **kwargs)
    sys.exit(app.exec_())

if __name__ == '__main__':
    label1 = time.time()
    label2 = 123
    label3 = "My name is Ahmed"
    my_dict = {
        "label1": label1, 
        "label2": label2, 
        "label3": label3
        }
    Thread(target=main, args=(), kwargs=my_dict, daemon=True).start()
    while flag:
        # print(my_dict)
        label2 += 1
        # print(label2)
        time.sleep(1)