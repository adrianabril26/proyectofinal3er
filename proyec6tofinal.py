import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# -------------------------
# FUNCIONES
# -------------------------
def abrir_registro_productos():   
   reg = tk.Toplevel()
   reg.title("Registro de Productos")
   reg.geometry("400x400")
   reg.resizable(False, False)

   # --- Etiquetas y Campos de Texto ---
   lbl_id = tk.Label(reg, text="ID del Producto:", font=("Arial", 12))
   lbl_id.pack(pady=5)
   txt_id = tk.Entry(reg, font=("Arial", 12))
   txt_id.pack(pady=5)
   lbl_desc = tk.Label(reg, text="Descripción:", font=("Arial", 12))
   lbl_desc.pack(pady=5)
   txt_desc = tk.Entry(reg, font=("Arial", 12))
   txt_desc.pack(pady=5)
   lbl_precio = tk.Label(reg, text="Precio:", font=("Arial", 12))
   lbl_precio.pack(pady=5)
   txt_precio = tk.Entry(reg, font=("Arial", 12))
   txt_precio.pack(pady=5)
   lbl_categoria = tk.Label(reg, text="Categoría:", font=("Arial", 12))
   lbl_categoria.pack(pady=5)
   txt_categoria = tk.Entry(reg, font=("Arial", 12))
   txt_categoria.pack(pady=5)

   # --- Función para guardar ---
   def guardar_producto():
      id_prod = txt_id.get().strip()
      descripcion = txt_desc.get().strip()
      precio = txt_precio.get().strip()
      categoria = txt_categoria.get().strip()
      # Validaciones
      if id_prod == "" or descripcion == "" or precio == "" or categoria == "":
         messagebox.showwarning("Campos Vacíos", "Por favor complete todos los campos.")
         return
      # Validar precio como número
      try:
         float(precio)
      except:
         messagebox.showerror("Error", "El precio debe ser un número.")
         return

      # Guardar en archivo de texto
      BASE_DIR = os.path.dirname(os.path.abspath(__file__))
      archivo = os.path.join(BASE_DIR,"productos.txt")
      with open(archivo, "a", encoding="utf-8") as archivo:
         archivo.write(f"{id_prod}|{descripcion}|{precio}|{categoria}\n")
         messagebox.showinfo("Guardado", "Producto registrado correctamente.")
         # Limpiar campos
         txt_id.delete(0, tk.END)
         txt_desc.delete(0, tk.END)
         txt_precio.delete(0, tk.END)
         txt_categoria.delete(0, tk.END)
   # --- Botón Guardar ---
   btn_guardar = ttk.Button(reg, text="Guardar Producto", command=guardar_producto)
   btn_guardar.pack(pady=20)

from datetime import datetime

def mostrar_ticket(producto, precio, cantidad, total):
  ticket = tk.Toplevel()
  ticket.title("Ticket de Venta")
  ticket.geometry("300x350")
  ticket.resizable(False, False)

  # --- SOLO AÑADIDO ---
  try:
      img = tk.PhotoImage(file="ventas2025.png")  # tu imagen
      lbl_img = tk.Label(ticket, image=img)
      lbl_img.image = img                  # evita que Tk la limpie
      lbl_img.pack()
  except Exception as e:
      print("Error cargando imagen:", e)
  # --------------------

  fecha_hora = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

  texto = (
  " *** PUNTO DE VENTA ***\n"
  "--------------------------------------\n"
  f"Fecha: {fecha_hora}\n"
  "--------------------------------------\n"
  f"Producto: {producto}\n"
  f"Precio: ${precio}\n"
  f"Cantidad: {cantidad}\n"
  "--------------------------------------\n"
  f"TOTAL: ${total}\n"
  "--------------------------------------\n"
  " ¡GRACIAS POR SU COMPRA!\n"
  )

  lbl_ticket = tk.Label(ticket, text=texto, justify="left", font=("Consolas", 11))
  lbl_ticket.pack(pady=15)

  btn_cerrar = ttk.Button(ticket, text="Cerrar", command=ticket.destroy)
  btn_cerrar.pack(pady=10)

  messagebox.showinfo("Venta Registrada", "La venta se registró correctamente.")



  

def abrir_registro_ventas():
   ven = tk.Toplevel()
   ven.title("Registro de Ventas")
   ven.geometry("420x430")
   ven.resizable(False, False)
   # ------------------------------------
   # Cargar productos desde productos.txt
   # ------------------------------------
   productos = {}
   try:
      BASE_DIR = os.path.dirname(os.path.abspath(__file__))
      archivof = os.path.join(BASE_DIR,"productos.txt")
      with open(archivof, "r", encoding="utf-8") as archivo:
         for linea in archivo:
            partes = linea.strip().split("|")
            if len(partes) == 4:
               idp, desc, precio, cat = partes
               productos[desc] = float(precio)
   except FileNotFoundError:
      messagebox.showerror("Error", "No se encontró el archivo productos.txt")
      ven.destroy()
      return

   # Lista de nombres de productos
   lista_productos = list(productos.keys())
   # ------------------------------------
   # CONTROLES VISUALES
   # ------------------------------------
   lbl_prod = tk.Label(ven, text="Producto:", font=("Arial", 12))
   lbl_prod.pack(pady=5)
   cb_producto = ttk.Combobox(ven, values=lista_productos, font=("Arial", 12), state="readonly")
   cb_producto.pack(pady=5)
   lbl_precio = tk.Label(ven, text="Precio:", font=("Arial", 12))
   lbl_precio.pack(pady=5)
   txt_precio = tk.Entry(ven, font=("Arial", 12), state="readonly")
   txt_precio.pack(pady=5)
   lbl_cantidad = tk.Label(ven, text="Cantidad:", font=("Arial", 12))
   lbl_cantidad.pack(pady=5)
   cantidad_var = tk.StringVar(ven)
   ven.cantidad_var = cantidad_var   # importante: mantiene la referencia
   txt_cantidad = tk.Entry(ven, font=("Arial", 12), textvariable=cantidad_var)
   txt_cantidad.pack(pady=5)  
   cantidad_var.trace_add("write", lambda *args: calcular_total())
   lbl_total = tk.Label(ven, text="Total:", font=("Arial", 12))
   lbl_total.pack(pady=5)
   txt_total = tk.Entry(ven, font=("Arial", 12), state="readonly")
   txt_total.pack(pady=5)
   # ------------------------------------
   # FUNCIONES
   # ------------------------------------
   def actualizar_precio(event):      
      prod = cb_producto.get()
      if prod in productos:
         txt_precio.config(state="normal")
         txt_precio.delete(0, tk.END)
         txt_precio.insert(0, productos[prod])
         txt_precio.config(state="readonly")
         calcular_total()
   def calcular_total(*args):      
      try:
         cant = int(txt_cantidad.get())
         precio = float(txt_precio.get())
         total = cant * precio
         txt_total.config(state="normal")
         txt_total.delete(0, tk.END)
         txt_total.insert(0, total)
         txt_total.config(state="readonly")
      except:
         # Si no hay número válido, limpiar el total
         txt_total.config(state="normal")
         txt_total.delete(0, tk.END)
         txt_total.config(state="readonly")
   def registrar_venta():
      prod = cb_producto.get()
      precio = txt_precio.get()
      cant = txt_cantidad.get()
      total = txt_total.get()
      if prod == "" or precio == "" or cant == "" or total == "":
         messagebox.showwarning("Campos Vacíos", "Todos los campos deben estar completos.")
         
         return
      # Guardar venta
      BASE_DIR = os.path.dirname(os.path.abspath(__file__))
      archivov = os.path.join(BASE_DIR,"ventas.txt")
      with open(archivov, "a", encoding="utf-8") as archivo:
         archivo.write(f"{prod}|{precio}|{cant}|{total}\n")
         messagebox.showinfo("Venta Registrada", "La venta se registró correctamente.")
         mostrar_ticket(prod, precio, cant, total)
      # Limpiar campos
      cb_producto.set("")
      txt_precio.config(state="normal"); txt_precio.delete(0, tk.END); txt_precio.config(state="readonly")
      txt_cantidad.delete(0, tk.END)
      txt_total.config(state="normal"); txt_total.delete(0, tk.END); txt_total.config(state="readonly")
   # ------------------------------------
   # EVENTOS Y BOTÓN
   # ------------------------------------
   cb_producto.bind("<<ComboboxSelected>>", actualizar_precio)
   btn_guardar = ttk.Button(ven, text="Registrar Venta", command=registrar_venta)
   btn_guardar.pack(pady=25)


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
