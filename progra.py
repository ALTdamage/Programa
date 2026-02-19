import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

# ----------------------------
# BASE DE DATOS#333
# ----------------------------

conexion = sqlite3.connect("finanzas.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    monto REAL,
    fecha TEXT
)
""")
conexion.commit()

# ----------------------------
# FUNCIONES
# ----------------------------

def calcular_saldo():
    cursor.execute("SELECT tipo, monto FROM movimientos")
    movimientos = cursor.fetchall()

    saldo = 0
    for tipo, monto in movimientos:
        if tipo == "Ingreso":
            saldo += monto
        else:
            saldo -= monto

    return saldo


def mostrar_movimientos():
    for fila in tabla.get_children():
        tabla.delete(fila)

    cursor.execute("SELECT tipo, monto, fecha FROM movimientos ORDER BY id DESC")
    movimientos = cursor.fetchall()

    for mov in movimientos:
        tabla.insert("", tk.END, values=mov)


def agregar_ingreso():
    try:
        monto = float(entry_monto.get())
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO movimientos (tipo, monto, fecha) VALUES (?, ?, ?)",
            ("Ingreso", monto, fecha)
        )
        conexion.commit()

        messagebox.showinfo("Éxito", "Ingreso guardado correctamente")
        entry_monto.delete(0, tk.END)
        actualizar_saldo()
        mostrar_movimientos()

    except:
        messagebox.showerror("Error", "Ingresa un número válido")


def agregar_gasto():
    try:
        monto = float(entry_monto.get())
        saldo_actual = calcular_saldo()

        if saldo_actual <= 0:
            messagebox.showerror("Error", "No tienes saldo disponible")
            return

        if monto > saldo_actual:
            messagebox.showerror("Error", "No puedes retirar más de lo que tienes")
            return

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO movimientos (tipo, monto, fecha) VALUES (?, ?, ?)",
            ("Gasto", monto, fecha)
        )
        conexion.commit()

        messagebox.showinfo("Éxito", "Gasto registrado correctamente")
        entry_monto.delete(0, tk.END)
        actualizar_saldo()
        mostrar_movimientos()

    except:
        messagebox.showerror("Error", "Ingresa un número válido")


def actualizar_saldo():
    saldo = calcular_saldo()
    label_saldo.config(text=f"Saldo actual: ${saldo:.2f}")


# ----------------------------
# INTERFAZ
# ----------------------------

ventana = tk.Tk()
ventana.title("Your Wallet")
ventana.geometry("700x600")
ventana.resizable(False, False)

titulo = tk.Label(ventana, text="Control de Finanzas", font=("Times New Roman", 22))
titulo.pack(pady=10)

entry_monto = tk.Entry(ventana, font=("Arial", 14))
entry_monto.pack(pady=10)

boton_ingreso = tk.Button(
    ventana,
    text="Agregar Ingreso",
    width=20,
    bg="#ADD8E6",
    fg="black",
    command=agregar_ingreso
)
boton_ingreso.pack(pady=5)

boton_gasto = tk.Button(
    ventana,
    text="Agregar Gasto",
    width=20,
    bg="#ADD8E6",
    fg="black",
    command=agregar_gasto
)
boton_gasto.pack(pady=5)

boton_salida = tk.Button(
    ventana,
    text="Salir",
    width=20,
    bg="#ADD8E6",
    fg="BLUE",
    command=ventana.destroy
)
boton_salida.pack(pady=5)

label_saldo = tk.Label(
    ventana,
    text="Saldo actual: $0.00",
    font=("Times New Roman", 14)
)
label_saldo.pack(pady=10)

# ----------------------------
# TABLA DE MOVIMIENTOS
# ----------------------------

tabla = ttk.Treeview(ventana, columns=("Tipo", "Monto", "Fecha"), show="headings")
tabla.heading("Tipo", text="Tipo")
tabla.heading("Monto", text="Monto")
tabla.heading("Fecha", text="Fecha y Hora")

tabla.column("Tipo", width=100, anchor="center")
tabla.column("Monto", width=100, anchor="center")
tabla.column("Fecha", width=200, anchor="center")

tabla.pack(pady=20)

actualizar_saldo()
mostrar_movimientos()

ventana.mainloop()
