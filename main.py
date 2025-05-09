import tkinter as tk
from tkinter import ttk
from componentes.ObjetoCard import ObjetoCard
from componentes.VentanaConstruccion import VentanaConstruccion
from PIL import Image, ImageTk
import json

# Cargar las piezas desde un JSON
with open("objetos.json", "r") as file:
    objetos = json.load(file)
class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selecciona un Objeto")
        self.geometry("900x500")
        self.configure(bg="#dcdcdc")

        label_ip = tk.Label(self, text="Direccion IP:", font=("Arial", 12), bg="#dcdcdc")
        label_ip.pack(pady=(10, 0))

        self.combo_box = ttk.Combobox(self, values=["192.168.1.111", "192.168.1.112", "192.168.1.114"])
        self.combo_box.pack()

        cards_frame = tk.Frame(self, bg="#dcdcdc")
        cards_frame.pack(pady=20)

        col = 0
        for objeto_id, pasos in objetos.items():
            estado = "disponible"  # o cargarlo desde otro JSON si lo tienes
            card = ObjetoCard(cards_frame, objeto_id, pasos, estado, on_armar=self.abrir_ventana)
            card.grid(row=0, column=col, padx=15, pady=10)
        col += 1

    def abrir_ventana(self, objeto_id):
        pasos = objetos[objeto_id]
        VentanaConstruccion(self, objeto_id, pasos)

    def selec_ip(self,evento):
        ip_select = combo_box.get()
        label_ip.config(text="Selected Item: " + ip_select)

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()

    

