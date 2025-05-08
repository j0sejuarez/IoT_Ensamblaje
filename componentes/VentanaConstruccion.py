import tkinter as tk
from PIL import Image, ImageTk
import threading
import serial
import time
from tkinter import messagebox

class VentanaConstruccion(tk.Toplevel):
    def __init__(self, master, objeto, pasos, puerto_serial="COM5", baudrate=115200):
        super().__init__(master)
        self.title(f"Construcción del {objeto}")
        self.geometry("900x500")
        self.configure(bg="#1e1e1e")

        self.pasos = pasos
        self.paso_actual = 0

        try:
            self.serial = serial.Serial(puerto_serial, baudrate, timeout=1)
            time.sleep(2)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al ESP32: {e}")
            self.destroy()
            return

        self.escuchando = True
        threading.Thread(target=self.escuchar_serial, daemon=True).start()

        # Encabezado
        header = tk.Frame(self, bg="black", height=40)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Button(header, text="⬅", font=("Arial", 12), command=self.cerrar_ventana,
                  bg="black", fg="white", borderwidth=0).pack(side=tk.LEFT, padx=10)
        tk.Label(header, text=f"Construcción del {objeto}", fg="white",
                 bg="black", font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        self.main_frame = tk.Frame(self, bg="#d9d9d9")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.left_panel = tk.Frame(self.main_frame, bg="#d9d9d9")
        self.left_panel.pack(side=tk.LEFT, padx=10)

        self.right_panel = tk.Frame(self.main_frame, bg="white", width=400, height=300)
        self.right_panel.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        self.lbl_info = tk.Label(self.right_panel, text="", font=("Arial", 12), bg="white")
        self.lbl_info.pack(pady=10)

        self.img_label = tk.Label(self.right_panel, bg="white")
        self.img_label.pack()

        self.mostrar_paso()

    def cerrar_ventana(self):
        self.escuchando = False
        if self.serial.is_open:
            self.serial.close()
        self.destroy()

    def cargar_imagen(self, ruta, tamaño=(100, 100)):
        img = Image.open(ruta).resize(tamaño)
        return ImageTk.PhotoImage(img)

    def mostrar_paso(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()

        if self.paso_actual >= len(self.pasos):
            self.lbl_info.config(text="✅ Objeto completado")
            self.img_label.config(image="")
            return

        paso = self.pasos[self.paso_actual]

        if paso["tipo"] == "construccion":
            for pieza in [paso["p1"], paso["p2"]]:
                card = tk.Frame(self.left_panel, bg="white", padx=5, pady=5)
                card.pack(pady=10)
                tk.Label(card, text=f"Pieza: {pieza['pieza']}", font=("Arial", 10), bg="white").pack()
                img = self.cargar_imagen(pieza["imagen"], (80, 80))
                label = tk.Label(card, image=img, bg="white")
                label.image = img
                label.pack()

            self.lbl_info.config(text=f"Ensamblando: {paso['cons']['pieza']}")
            img = self.cargar_imagen(paso["cons"]["imagen"], (200, 200))
            self.img_label.config(image=img)
            self.img_label.image = img

            self.codigo_esperado = paso["p1"]["codigo"]
            self.serial.write((self.codigo_esperado + "\n").encode())

        elif paso["tipo"] == "resultado":
            self.lbl_info.config(text=f"Pieza final: {paso['pieza']['pieza']}")
            img = self.cargar_imagen(paso["pieza"]["imagen"], (200, 200))
            self.img_label.config(image=img)
            self.img_label.image = img

            self.codigo_esperado = paso["pieza"]["codigo"]
            self.serial.write((self.codigo_esperado + "\n").encode())

    def escuchar_serial(self):
        while self.escuchando:
            try:
                if self.serial.in_waiting > 0:
                    linea = self.serial.readline().decode().strip()
                    if linea:
                        self.after(0, self.validar_boton, linea)
                time.sleep(0.1)
            except Exception as e:
                print("Error al leer Serial:", e)
                break

    def validar_boton(self, pieza_recibida):
        if self.paso_actual >= len(self.pasos):
            return

        if pieza_recibida == self.codigo_esperado:
            self.paso_actual += 1
            self.mostrar_paso()
        else:
            messagebox.showwarning("Error", f"Pieza incorrecta: {pieza_recibida}. Esperada: {self.codigo_esperado}")
