import tkinter as tk
from PIL import Image, ImageTk
import threading
import serial
import time
from tkinter import messagebox

class VentanaConstruccion(tk.Toplevel):
    def __init__(self, master, objeto, pasos, puerto_serial="COM3", baudrate=115200):
        super().__init__(master)
        self.title(f"Construcción del {objeto}")
        self.state("zoomed")
        self.configure(bg="#1e1e1e")
        self.objeto = objeto
        self.pasos = pasos
        self.paso_actual = 0
        self.codigo_esperado = ""

        try:
            self.serial = serial.Serial(puerto_serial, baudrate, timeout=1)
            time.sleep(2)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al ESP32: {e}")
            self.destroy()
            return

        self.escuchando = True
        threading.Thread(target=self.escuchar_serial, daemon=True).start()

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

        self.lbl_estado = tk.Label(self.right_panel, text="", font=("Arial", 10), bg="white", fg="blue")
        self.lbl_estado.pack(pady=5)

        self.img_label = tk.Label(self.right_panel, bg="white")
        self.img_label.pack()

        self.mostrar_paso()

    def cerrar_ventana(self):
        self.escuchando = False
        self.enviar_led("X")
        if self.serial.is_open:
            self.serial.close()
        self.destroy()

    def cargar_imagen(self, ruta, tamaño=(100, 100)):
        try:
            img = Image.open(ruta).resize(tamaño)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error al cargar imagen {ruta}: {e}")
            return None

    def enviar_led(self, numero):
        try:
            comando = f"L{numero}\n"
            self.serial.write(comando.encode())
            print(f"Enviando al ESP32: {comando.strip()}")
        except Exception as e:
            print(f"Error al enviar comando LED: {e}")

    def mostrar_paso(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()

        if self.paso_actual >= len(self.pasos):
            self.lbl_info.config(text="✅ Objeto completado")
            self.img_label.config(image="")
            self.enviar_led("4")  # LED 4 indica finalización
            return

        paso = self.pasos[self.paso_actual]
        self.enviar_led(self.paso_actual + 1 if self.paso_actual < 4 else 1)

        if paso["tipo"] == "construccion":
            for pieza in [paso["p1"], paso["p2"]]:
                card = tk.Frame(self.left_panel, bg="white", padx=5, pady=5)
                card.pack(pady=10)
                tk.Label(card, text=f"Pieza: {pieza['pieza']}", font=("Arial", 10), bg="white").pack()
                img = self.cargar_imagen(pieza["imagen"], (200, 200))
                if img:
                    label = tk.Label(card, image=img, bg="white")
                    label.image = img
                    label.pack()

            self.lbl_info.config(text=f"Ensamblando: {paso['cons']['pieza']}")
            img = self.cargar_imagen(paso["cons"]["imagen"], (800, 400))
            if img:
                self.img_label.config(image=img)
                self.img_label.image = img

            self.codigo_esperado = paso["p1"]["codigo"]

        elif paso["tipo"] == "resultado":
            self.lbl_info.config(text=f"Pieza final: {paso['pieza']['pieza']}")
            card = tk.Frame(self.left_panel, bg="white", padx=5, pady=5)
            card.pack(pady=10)
            tk.Label(card, text=f"Pieza Final: {paso['pieza']['pieza']}", font=("Arial", 10), bg="white").pack()
            img = self.cargar_imagen(paso["pieza"]["imagen"], (200, 200))
            label = tk.Label(card, image=img, bg="white")
            label.image = img
            label.pack()

            self.lbl_info.config(text=f"✅ Objeto completado: {paso['pieza']['pieza']}")
            img = self.cargar_imagen(paso["pieza"]["imagen"], (600, 500))
            self.img_label.config(image=img)
            self.img_label.image = img

            self.codigo_esperado = paso["pieza"]["codigo"]

    def avanzar_paso(self):
        self.paso_actual += 1
        self.lbl_estado.config(text="")
        self.mostrar_paso()

    def escuchar_serial(self):
        while self.escuchando:
            try:
                if self.serial.in_waiting > 0:
                    linea = self.serial.readline().decode().strip()
                    if linea:
                        self.after(0, self.validar_boton, linea)
                time.sleep(0.1)
            except Exception as e:
                print(f"Error al leer del puerto serial: {e}")
                self.escuchando = False
                break

    def validar_boton(self, codigo):
        self.lbl_estado.config(text=f"Código recibido: {codigo}", fg="blue")

        secuencia = ["1000", "1001", "1002", "1003", "1000"]
        if self.paso_actual < len(secuencia):
            esperado = secuencia[self.paso_actual]
            if codigo == esperado:
                self.lbl_estado.config(text=f"Paso {self.paso_actual + 1} correcto", fg="green")
                self.avanzar_paso()
            else:
                self.lbl_estado.config(text=f"Código incorrecto. Esperado: {esperado}", fg="red")
        else:
            self.lbl_estado.config(text=f"Secuencia completada.", fg="green")