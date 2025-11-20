import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# -------------------------
# FUNCIONES
# -------------------------
def abrir_registro_productos():
   messagebox.showinfo("Registro de Productos", "Aquí irá el módulo de registro de productos.")

def abrir_registro_ventas():
   messagebox.showinfo("Registro de Ventas", "Aquí irá el módulo de registro de ventas.")

def abrir_reportes():
   messagebox.showinfo("Reportes", "Aquí irá el módulo de reportes.")

def abrir_acerca_de():
   messagebox.showinfo("Acerca de", "Punto de Venta de Ropa\nProyecto Escolar\nVersión 1.0")

# -------------------------
# VENTANA PRINCIPAL
# -------------------------
ventana = tk.Tk()
ventana.title("Surelio Marciano")
ventana.state("zoomed")
ventana.resizable(False, False)

# Fondo basado en el espacio del logo
ventana.configure(bg="#0A1A3F")

# -------------------------
# LOGO
# -------------------------
try:
   BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   imagen = Image.open(os.path.join(BASE_DIR,"ventas2025.png"))
   imagen = imagen.resize((250, 250))
   img_logo = ImageTk.PhotoImage(imagen)

   lbl_logo = tk.Label(ventana, image=img_logo, bg="#0A1A3F")
   lbl_logo.pack(pady=20)
except:
   lbl_sin_logo = tk.Label(ventana, text="(Aquí va el logo)", 
                           font=("Arial", 14), bg="#0A1A3F", fg="#8EE082")
   lbl_sin_logo.pack(pady=40)

# -------------------------
# ESTILO "SURELIO MARCIANO"
# -------------------------
estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "Alien.TButton",
    font=("Arial", 14, "bold"),
    padding=12,
    background="#93E6E3",      # Turquesa nave espacial
    foreground="#2D2B60",      # Azul/morado del texto del logo
    borderwidth=3,
    relief="flat"
)

estilo.map(
    "Alien.TButton",
    background=[
        ("active", "#8CD4D2"),   # Hover turquesa
        ("pressed", "#7BBEC0")
    ],
    foreground=[("active", "#2D2B60")]
)

# -------------------------
# BOTONES
# -------------------------
btn_reg_prod = ttk.Button(ventana, text="Registro de Productos",
                          command=abrir_registro_productos, style="Alien.TButton")
btn_reg_prod.pack(pady=12)

btn_reg_ventas = ttk.Button(ventana, text="Registro de Ventas",
                            command=abrir_registro_ventas, style="Alien.TButton")
btn_reg_ventas.pack(pady=12)

btn_reportes = ttk.Button(ventana, text="Reportes",
                          command=abrir_reportes, style="Alien.TButton")
btn_reportes.pack(pady=12)

btn_acerca = ttk.Button(ventana, text="Acerca de",
                        command=abrir_acerca_de, style="Alien.TButton")
btn_acerca.pack(pady=12)

# -------------------------
# INICIO DE LA APP
# -------------------------
ventana.mainloop()
