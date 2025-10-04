import sys
from threading import Thread
from typing import Any
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTabWidget, QCheckBox, QComboBox,
    QRadioButton, QGroupBox, QButtonGroup, QSpinBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer

flag = True

class MainWindow(QMainWindow):
    def __init__(self, *args, caller_globals=None, tracked_dict=None, **kwargs):
        super().__init__()
        self.setWindowTitle('Trace GUI')
        self.setCentralWidget(QWidget())
        self.hbox1 = QHBoxLayout(self.centralWidget())
        self.vbox1 = QVBoxLayout(self.centralWidget())

        # Use the caller's global namespace and tracked dictionary
        self.glbl = caller_globals or {}
        self.tracked_dict = tracked_dict or kwargs
        self.labels = {}

        self.setStyleSheet(
            "QLabel{border: 2px solid black; border-radius: 5px; margin: 5px;}"
            "QHBoxLayout{border: 2px solid black; border-radius: 5px; margin: 5px;}"
            "QVBoxLayout{border: 2px solid black; border-radius: 5px; margin: 5px;}"
        )

        self.initUI()
        self.trace(*args, **kwargs)
        # Use QTimer for safe GUI updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Update every 1000ms
        self.show()

    def initUI(self):
        self.vbox.addLayout(self.hbox1)
        for key in self.tracked_dict:
            value = self.glbl.get(key, self.tracked_dict[key])
            label = QLabel(f"{key}: {value}", self)
            self.labels[key] = label
            self.hbox1.addWidget(label)

    def update(self):
        for key, label in self.labels.items():
            # Check glbl first, fall back to tracked_dict
            value = self.glbl.get(key, self.tracked_dict[key])
            label.setText(f"{key}: {value}")

    def trace(self, *args, **kwargs):
        # Update tracked_dict with initial kwargs if not provided
        for k, v in kwargs.items():
            if k not in self.tracked_dict:
                self.tracked_dict[k] = v

    def closeEvent(self, event):
        global flag
        flag = False
        self.timer.stop()  # Stop the timer when closing
        event.accept()

def run_gui(*args, caller_globals=None, tracked_dict=None, **kwargs):
    global window1
    app = QApplication(sys.argv)
    window1 = MainWindow(*args, caller_globals=caller_globals, tracked_dict=tracked_dict, **kwargs)
    app.exec_()  # Run the event loop without sys.exit

def main(*args, caller_globals=None, tracked_dict=None, **kwargs):
    # Start the GUI in a separate daemon thread
    Thread(target=run_gui, args=args, kwargs={"caller_globals": caller_globals, "tracked_dict": tracked_dict, **kwargs}, daemon=True).start()
    # Return immediately to allow the importing script to continue
    return