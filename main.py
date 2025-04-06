import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json

# Cargar las piezas desde un JSON
with open("objetos.json", "r") as file:
    objetos = json.load(file)

class VentanaConstruccion(tk.Toplevel):
    def __init__(self, master, objeto, piezas):
        super().__init__(master)
        self.title(f"Construcción del {objeto}")
        self.geometry("500x400")

        self.piezas = piezas
        self.pieza_actual = 0

        # Etiqueta de pieza
        self.label_pieza = tk.Label(self, text=f"Pieza: {self.piezas[self.pieza_actual]['pieza']}", font=("Arial", 14))
        self.label_pieza.pack(pady=10)

        # Imagen de la pieza
        self.img_label = tk.Label(self)
        self.img_label.pack()
        self.mostrar_imagen()

        # Botón para siguiente pieza
        self.btn_siguiente = tk.Button(self, text="Siguiente", command=self.mostrar_siguiente)
        self.btn_siguiente.pack(pady=10)

    def mostrar_imagen(self):
        img_path = self.piezas[self.pieza_actual]["imagen"]
        img = Image.open(img_path).resize((200, 200))
        self.img_tk = ImageTk.PhotoImage(img)
        self.img_label.config(image=self.img_tk)

    def mostrar_siguiente(self):
        self.pieza_actual += 1
        if self.pieza_actual < len(self.piezas):
            self.label_pieza.config(text=f"Pieza: {self.piezas[self.pieza_actual]['pieza']}")
            self.mostrar_imagen()
        else:
            self.label_pieza.config(text=f"Objeto completado: {self.piezas[-1]['pieza']}")
            self.img_label.config(image="")
            self.btn_siguiente.config(state=tk.DISABLED)

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selecciona un Objeto")
        self.geometry("300x200")
        label_ip = tk.Label(self, text="Direccion IP:", font=("Arial", 12)).pack()
        combo_box = ttk.Combobox(self, values=["192.168.1.111", "192.168.1.112", "192.168.1.114"]).pack()
        tk.Label(self, text="Elige un objeto:", font=("Arial", 12)).pack(pady=10)

        for objeto in objetos.keys():
            tk.Button(self, text=objeto, command=lambda obj=objeto: self.abrir_ventana(obj)).pack(pady=5)

    def abrir_ventana(self, objeto):
        VentanaConstruccion(self, objeto, objetos[objeto])

    def selec_ip(self,evento):
        ip_select = combo_box.get()
        label_ip.config(text="Selected Item: " + ip_select)


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

    

