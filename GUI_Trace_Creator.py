from tkinter import * # type: ignore
from tkinter import messagebox
# from typing import Any 
from threading import Thread



class LabelEntry(Frame):    
    
    def __init__(self, master, text, variable, coord, change = False, *args, **kwargs):
        self.text = text
        self.variable = variable
        self.label = Label(master, text=f"{self.text} = {self.variable:.2f}", font=("Arial", 12))
        self.label.grid(row=coord[0], column=coord[1], sticky=W)
        if change: 
            self.entry = Entry(master, *args, **kwargs)
            self.entry.insert(0, str(variable))
            self.entry.grid(row=coord[0], column=coord[1]+1, padx=5, pady=5)
            self.button = Button(master, text="Change", font=("Arial", 12), command=self.change)
            self.button.grid(row=coord[0], column=coord[1]+2, padx=5, pady=5)

    def update(self, new_value) -> None:
        self.variable = new_value
        self.label.config(text=f"{self.text} = {self.variable:.2f}")

    def change(self) -> None:
        try:
            new_value = type(self.variable)(self.entry.get())
            self.update(new_value)
            pop_up = messagebox.showinfo("Success", f"{self.text} changed to {self.variable} successfully!")
            print(f"\rChanged to {self.variable}", "   " * 10, end="\r")
        except:
            pop_up = messagebox.showerror("Error", "Invalid input")
            print("\rInvalid input", "   " * 10, end="\r")

class CreateGui():

    def __init__(self, gui_type, *args, **kwargs):
        self.gui_type = gui_type
        self.args = args
        self.kwargs = kwargs

        self.root = Tk()
        self.root.title("Trace GUI")
        self.general_canvas = Canvas(self.root)
        self.general_canvas.pack()
        self.sub_canvases = {}
        for i in kwargs.keys():
            self.sub_canvases[i] = Canvas(self.root)
            self.sub_canvases[i].pack(side = RIGHT)

        self.labels = {}
        for i,j in enumerate(args):
            self.labels[i] = LabelEntry(self.general_canvas, j, j, (i, 0))

        for name, value in kwargs.items():
            for i, j in enumerate(value[1].items()):
                self.labels[name] = LabelEntry(self.sub_canvases[name], j[0], j[1], (i, 0), change=value[0])

        self.root.protocol("WM_DELETE_WINDOW", self.closing)

    def run(self):
        self.root.mainloop()

    def closing(self):
        global flag
        flag = False
        self.root.destroy()

v = 500

if __name__ == "__main__":
    flag = True
    my_gui = CreateGui("Hello", v, car=(True, {'height': 5, 'width': 2, 'speed': 0}))
    # while flag:
    my_gui.run()
        