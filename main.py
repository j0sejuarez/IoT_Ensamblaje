import tkinter as tk
from tkinter import Frame, Label, Button

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Ensamblaje")
        self.geometry("800x600")
        self.configure(bg="gray")
        self.current_frame = None

if __name__ == "__main__":
    app = App()
    app.mainloop()

