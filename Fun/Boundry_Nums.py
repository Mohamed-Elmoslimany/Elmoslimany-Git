import sys
from threading import Thread
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # type: ignore
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt

plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': '#222222',
    'axes.facecolor': '#000000',
    'axes.edgecolor': '#888888',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'grid.color': '#444444',
    'text.color': 'white'
})

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('')
        self.resize(800, 400)
        self.show()
        self.setStyleSheet(
            'QMainWindow{background-color: #1f1f1f;}'
            'QLabel{border: 2px solid gray; margin: 5px; border-radius: 10px; font-size: 20px; color: #ffffff; background-color: #444444;}'
            'QLineEdit{border: 2px solid gray; margin: 5px; border-radius: 10px; font-size: 20px; color: #ffffff; background-color: #444444;}'
                           )

        self.canvas = MplCanvas(self, width=7, height=4, dpi=100, )
        self.canvas.axes.plot([0, 1, 2, 3], [10, 1, 20, 3])
        self.canvas.axes.set_title("Example Plot")

        self.change_starting_num = QLineEdit(self)
        self.change_starting_num.setPlaceholderText("Enter value")
        self.change_starting_num.returnPressed.connect(self.on_line_edit)

        self.trace_labels = {
            'starting_num': QLabel(self),
            # 'current_num': QLabel(self),
            # 'next_num': QLabel(self),
            'highest_num': QLabel(self),
            'steps': QLabel(self),
            'repeated_steps': QLabel(self),
            'loop_list': QLabel(self),
            'nums_list': QLabel(self),
        }
        # self.trace_labels['nums_list'].setMaximumWidth(200)
        self.trace_labels['nums_list'].setWordWrap(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_trace_labels)
        self.timer.start(100)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.hbox = QHBoxLayout(central_widget)
        self.hbox.addWidget(self.canvas)

        self.vbox = QVBoxLayout(central_widget)
        self.vbox.addWidget(self.change_starting_num)
        for label in self.trace_labels.values():
            self.vbox.addWidget(label)
        self.hbox.addLayout(self.vbox)

    def on_line_edit(self):
        global starting_num, current_num, next_num, highest_num, steps, repeated_steps, loop_list, nums_list, step_list, flag
        starting_num = int(self.change_starting_num.text())
        self.change_starting_num.clear()
        current_num = starting_num
        next_num = 0
        highest_num = current_num
        steps = 0
        repeated_steps = 0
        loop_list = set()
        flag = 0
        nums_list = [current_num]
        step_list = [0]
        flag = 0

        update()

    def update_trace_labels(self):
        self.trace_labels['starting_num'].setText(f"Starting Number: {starting_num}")
        # self.trace_labels['current_num'].setText(f"Current Number: {current_num}")
        # self.trace_labels['next_num'].setText(f"Next Number: {next_num}")
        self.trace_labels['highest_num'].setText(f"Highest Number: {highest_num}")
        self.trace_labels['steps'].setText(f"Steps: {steps}")
        self.trace_labels['repeated_steps'].setText(f"Repeated Steps: {len(loop_list)}")
        self.trace_labels['loop_list'].setText(f"Loop List: {loop_list}")
        self.trace_labels['nums_list'].setText(f"Nums List: {nums_list}")
        self.canvas.axes.clear()
        self.canvas.axes.plot(step_list, nums_list, marker='o')
        self.canvas.draw()

starting_num = 1
current_num = 1
next_num = 0
highest_num = 0
steps = 0
repeated_steps = 0
loop_list = set()
flag = 0
nums_list = []
step_list = []

def get_factors(num):
    factors = []
    if num == 1 or num == 0:
        return factors
    for i in range(1, num):
        if num % i == 0:
            factors.append(i)
    return factors

def next_step():
    global starting_num, current_num, next_num, highest_num, steps, repeated_steps, loop_list, flag
    next_num = sum(get_factors(current_num))
    if next_num > highest_num:
        highest_num = next_num
    if (next_num == starting_num or next_num in nums_list) and not flag:
        repeated_steps += 1
        flag = 1
    if repeated_steps:
        loop_list.add(current_num)
    if next_num == starting_num and flag or next_num == current_num or next_num == 0 or next_num in nums_list:
        flag += 3
    if next_num > 10**7:
        flag = 3
    current_num = next_num

    steps += 1
    nums_list.append(current_num)
    step_list.append(steps)
    return next_num

def main():
    global app, window1
    app = QApplication(sys.argv)
    window1 = MainWindow()
    app.exec_()

def update():
    while window1.isVisible():
        next_step()
        print(f"Step {steps}: {current_num}\nHighest: {highest_num}\nRepeats: {repeated_steps}\nLoop: {loop_list}\nFlag: {flag}\nnums_list: {nums_list}\nstep_list: {step_list}\n")
        if flag == 25 or flag == 3:
            break
        time.sleep(0.1)

if __name__ == '__main__':
    # Thread(main(), daemon=True).start()
    # starting_num = int(input("Enter a number: "))
    # current_num = starting_num
    main()
    update()