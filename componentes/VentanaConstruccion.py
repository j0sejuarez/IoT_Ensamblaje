import tkinter as tk
from PIL import Image, ImageTk
import json

def procesar_json(json_data):
    piezas = json_data["Llave"]
    pasos = []
    i = 0
    while i < len(piezas):
        if piezas[i]["pieza"].isdigit():
            p1 = piezas[i]
            p2 = piezas[i+1]
            cons = piezas[i+2]
            pasos.append({
                "tipo": "construccion",
                "p1": p1,
                "p2": p2,
                "cons": cons
            })
            pasos.append({
                "tipo": "resultado",
                "pieza": piezas[i+3]
            })
            i += 4
        else:
            i += 1
    return pasos

class VentanaConstruccion(tk.Toplevel):
    def __init__(self, master, objeto, pasos):
        super().__init__(master)
        self.title(f"Construcción del {objeto}")
        self.geometry("900x500")
        self.configure(bg="#1e1e1e")

        self.pasos = pasos
        self.paso_actual = 0

        # Header
        header = tk.Frame(self, bg="black", height=40)
        header.pack(side=tk.TOP, fill=tk.X)

        btn_back = tk.Button(header, text="⬅", font=("Arial", 12), command=self.destroy,
                             bg="black", fg="white", borderwidth=0)
        btn_back.pack(side=tk.LEFT, padx=10)

        lbl_title = tk.Label(header, text=f"Construccion del {objeto}", fg="white",
                             bg="black", font=("Arial", 12, "bold"))
        lbl_title.pack(side=tk.LEFT)

        # Main layout
        self.main_frame = tk.Frame(self, bg="#d9d9d9")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Panel izquierdo
        self.left_panel = tk.Frame(self.main_frame, bg="#d9d9d9")
        self.left_panel.pack(side=tk.LEFT, padx=10)

        # Panel central (pieza combinada o final)
        self.right_panel = tk.Frame(self.main_frame, bg="white", width=400, height=300)
        self.right_panel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        self.lbl_info = tk.Label(self.right_panel, text="", font=("Arial", 12), bg="white")
        self.lbl_info.pack(pady=10)

        self.img_label = tk.Label(self.right_panel, bg="white")
        self.img_label.pack()

        self.btn_siguiente = tk.Button(self.right_panel, text="Siguiente", command=self.siguiente_paso)
        self.btn_siguiente.pack(pady=10)

        self.mostrar_paso()

    def cargar_imagen(self, ruta, tamaño=(100, 100)):
        img = Image.open(ruta).resize(tamaño)
        return ImageTk.PhotoImage(img)

    def mostrar_paso(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()

        paso = self.pasos[self.paso_actual]

        if paso["tipo"] == "construccion":
            # Mostrar 2 piezas pequeñas a la izquierda
            for pieza in [paso["p1"], paso["p2"]]:
                card = tk.Frame(self.left_panel, bg="white", padx=5, pady=5)
                card.pack(pady=10)

                label = tk.Label(card, text=f"Pieza: {pieza['pieza']}", font=("Arial", 10), bg="white")
                label.pack()

                img = self.cargar_imagen(pieza["imagen"], (80, 80))
                img_label = tk.Label(card, image=img, bg="white")
                img_label.image = img
                img_label.pack()

            # Mostrar la construcción en grande
            self.lbl_info.config(text=f"Construcción de pieza: {paso['cons']['pieza']}")
            img = self.cargar_imagen(paso["cons"]["imagen"], (200, 200))
            self.img_label.config(image=img)
            self.img_label.image = img

        elif paso["tipo"] == "resultado":
            # Ocultar panel izquierdo
            self.lbl_info.config(text=f"Pieza: {paso['pieza']['pieza']}")
            img = self.cargar_imagen(paso["pieza"]["imagen"], (200, 200))
            self.img_label.config(image=img)
            self.img_label.image = img

    def siguiente_paso(self):
        self.paso_actual += 1
        if self.paso_actual < len(self.pasos):
            self.mostrar_paso()
        else:
            self.lbl_info.config(text="Objeto completado")
            self.img_label.config(image="")
            self.btn_siguiente.config(state=tk.DISABLED)