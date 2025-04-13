import tkinter as tk
from PIL import Image, ImageTk

class ObjetoCard(tk.Frame):
    def __init__(self, master, objeto_id, pasos, estado="disponible", on_armar=None, *args, **kwargs):
        super().__init__(master, bd=2, relief="groove", bg="white", *args, **kwargs)
        self.objeto_id = objeto_id
        self.estado = estado
        self.on_armar = on_armar

        self.config(width=180, height=240)
        self.grid_propagate(False)

        # Buscar imagen representativa del objeto (primera imagen encontrada en pasos)
        img_path = self.obtener_imagen_representativa(pasos)
        self.img_tk = self.cargar_imagen(img_path)
        self.label_img = tk.Label(self, image=self.img_tk, bg="white")
        self.label_img.pack(pady=10)

        # Nombre del objeto
        tk.Label(self, text=objeto_id, font=("Arial", 12, "bold"), bg="white").pack()

        # Estado visual
        lbl_estado = tk.Label(self, text=f"Estado: {self.estado}", font=("Arial", 10), bg="white", fg="green" if self.estado == "disponible" else "red")
        lbl_estado.pack()

        # Botón de armar
        self.btn_armar = tk.Button(self, text="Armar", command=self.armar)
        self.btn_armar.pack(pady=10)

        if self.estado != "disponible":
            self.btn_armar.config(state="disabled")

    def cargar_imagen(self, path):
        try:
            img = Image.open(path).resize((120, 120))
        except Exception:
            img = Image.new("RGB", (120, 120), color="gray")
        return ImageTk.PhotoImage(img)

    def obtener_imagen_representativa(self, pasos):
        for paso in pasos:
            if paso["tipo"] == "construccion":
                return paso["p1"]["imagen"]
            elif paso["tipo"] == "resultado":
                return paso["pieza"]["imagen"]
        return "placeholder.png"  # Por si no se encuentra nada

    def armar(self):
        if self.on_armar:
            self.on_armar(self.objeto_id)
