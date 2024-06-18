import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
import os

# Conexión a la base de datos SQLite
db_path = 'operadores_piezas.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Crear tablas
c.execute('''CREATE TABLE IF NOT EXISTS operadores (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS piezas (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS tiempos (
                id INTEGER PRIMARY KEY,
                operador_id INTEGER,
                pieza_id INTEGER,
                tiempo REAL,
                FOREIGN KEY (operador_id) REFERENCES operadores (id),
                FOREIGN KEY (pieza_id) REFERENCES piezas (id))''')

c.execute('''CREATE TABLE IF NOT EXISTS estado (
                id INTEGER PRIMARY KEY,
                operador_id INTEGER,
                pieza_id INTEGER,
                inicio REAL,
                FOREIGN KEY (operador_id) REFERENCES operadores (id),
                FOREIGN KEY (pieza_id) REFERENCES piezas (id))''')

conn.commit()

# Funciones
def agregar_operador():
    nombre = operador_entry.get()
    if nombre:
        c.execute("SELECT nombre FROM operadores WHERE nombre=?", (nombre,))
        if c.fetchone():
            messagebox.showwarning("Advertencia", "El nombre del operador ya existe.")
        else:
            c.execute("INSERT INTO operadores (nombre) VALUES (?)", (nombre,))
            conn.commit()
            actualizar_listas()
            operador_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "El nombre del operador no puede estar vacío.")

def eliminar_operador():
    nombre = operador_entry.get()
    if nombre:
        c.execute("DELETE FROM operadores WHERE nombre=?", (nombre,))
        conn.commit()
        actualizar_listas()
        operador_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "El nombre del operador no puede estar vacío.")

def agregar_pieza():
    nombre = pieza_entry.get()
    if nombre:
        c.execute("SELECT nombre FROM piezas WHERE nombre=?", (nombre,))
        if c.fetchone():
            messagebox.showwarning("Advertencia", "El nombre de la pieza ya existe.")
        else:
            c.execute("INSERT INTO piezas (nombre) VALUES (?)", (nombre,))
            conn.commit()
            actualizar_listas()
            pieza_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "El nombre de la pieza no puede estar vacío.")

def eliminar_pieza():
    nombre = pieza_entry.get()
    if nombre:
        c.execute("DELETE FROM piezas WHERE nombre=?", (nombre,))
        conn.commit()
        actualizar_listas()
        pieza_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "El nombre de la pieza no puede estar vacío.")

def actualizar_listas():
    operadores_listbox.delete(0, tk.END)
    piezas_listbox.delete(0, tk.END)
    c.execute("SELECT nombre FROM operadores")
    operadores = c.fetchall()
    for operador in operadores:
        operadores_listbox.insert(tk.END, operador[0])

    c.execute("SELECT nombre FROM piezas")
    piezas = c.fetchall()
    for pieza in piezas:
        piezas_listbox.insert(tk.END, pieza[0])

    for i in range(10):
        operadores_menu[i]["menu"].delete(0, "end")
        piezas_menu[i]["menu"].delete(0, "end")
        for operador in operadores:
            operadores_menu[i]["menu"].add_command(label=operador[0], command=tk._setit(operadores_seleccion[i], operador[0]))
        for pieza in piezas:
            piezas_menu[i]["menu"].add_command(label=pieza[0], command=tk._setit(piezas_seleccion[i], pieza[0]))

    consulta_operador_menu["menu"].delete(0, "end")
    consulta_pieza_menu["menu"].delete(0, "end")
    for operador in operadores:
        consulta_operador_menu["menu"].add_command(label=operador[0], command=tk._setit(consulta_operador, operador[0]))
    for pieza in piezas:
        consulta_pieza_menu["menu"].add_command(label=pieza[0], command=tk._setit(consulta_pieza, pieza[0]))

def iniciar_tiempo(index):
    operador = operadores_seleccion[index].get()
    pieza = piezas_seleccion[index].get()
    if operador and pieza:
        c.execute("SELECT id FROM operadores WHERE nombre=?", (operador,))
        operador_id = c.fetchone()[0]
        c.execute("SELECT id FROM piezas WHERE nombre=?", (pieza,))
        pieza_id = c.fetchone()[0]
        inicio = time.time()
        c.execute("INSERT INTO estado (operador_id, pieza_id, inicio) VALUES (?, ?, ?)", (operador_id, pieza_id, inicio))
        conn.commit()
        tiempos_inicio[index] = inicio
        botones_iniciar[index].config(bg="lightgreen")
        indicadores_tiempo[index].config(text="En marcha")
    else:
        messagebox.showwarning("Advertencia", "Debes seleccionar un operador y una pieza antes de iniciar el tiempo.")

def terminar_tiempo(index):
    if tiempos_inicio[index] is not None:
        tiempo_final = time.time()
        tiempo_total = tiempo_final - tiempos_inicio[index]
        operador = operadores_seleccion[index].get()
        pieza = piezas_seleccion[index].get()
        c.execute("SELECT id FROM operadores WHERE nombre=?", (operador,))
        operador_id = c.fetchone()[0]
        c.execute("SELECT id FROM piezas WHERE nombre=?", (pieza,))
        pieza_id = c.fetchone()[0]
        c.execute("INSERT INTO tiempos (operador_id, pieza_id, tiempo) VALUES (?, ?, ?)", (operador_id, pieza_id, tiempo_total))
        c.execute("DELETE FROM estado WHERE operador_id=? AND pieza_id=?", (operador_id, pieza_id))
        conn.commit()
        tiempos_inicio[index] = None
        botones_iniciar[index].config(bg="white")
        indicadores_tiempo[index].config(text="")
    else:
        messagebox.showwarning("Advertencia", "Debes iniciar el tiempo antes de terminarlo.")

def borrar_registro(index):
    operadores_seleccion[index].set('')
    piezas_seleccion[index].set('')
    indicadores_tiempo[index].config(text="")

def consultar_promedio():
    pieza = consulta_pieza.get()
    if pieza:
        c.execute("SELECT id FROM piezas WHERE nombre=?", (pieza,))
        pieza_id = c.fetchone()
        if pieza_id:
            c.execute("SELECT AVG(tiempo), COUNT(tiempo) FROM tiempos WHERE pieza_id=?", (pieza_id[0],))
            resultado_consulta = c.fetchone()
            promedio = resultado_consulta[0]
            conteo = resultado_consulta[1]
            if promedio and conteo:
                resultado_texto = f"Promedio de tiempo: {promedio:.2f} segundos (calculado en {conteo} veces)\n"
                # Mostrar el promedio de cada operador que ha hecho esa pieza
                c.execute("SELECT operadores.nombre, AVG(tiempos.tiempo) FROM tiempos JOIN operadores ON tiempos.operador_id=operadores.id WHERE pieza_id=? GROUP BY operador_id", (pieza_id[0],))
                promedios_operadores = c.fetchall()
                resultado_texto += "Promedio por operador:\n"
                for po in promedios_operadores:
                    resultado_texto += f"{po[0]}: {po[1]:.2f} segundos\n"
                resultado.set(resultado_texto)
            else:
                resultado.set("No hay datos suficientes para calcular el promedio.")
        else:
            resultado.set("Pieza no encontrada.")
    else:
        resultado.set("Debes seleccionar una pieza.")

# Interfaz gráfica
root = tk.Tk()
root.title("Registro de Tiempo de Operadores")

def on_closing():
    if messagebox.askokcancel("Salir", "¿Quieres salir?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Sección de agregar/eliminar operadores y piezas
frame_agregar = tk.Frame(root)
frame_agregar.pack(pady=10)

tk.Label(frame_agregar, text="Operador:").grid(row=0, column=0)
operador_entry = tk.Entry(frame_agregar)
operador_entry.grid(row=0, column=1)

tk.Button(frame_agregar, text="Agregar Operador", command=agregar_operador).grid(row=0, column=2)
tk.Button(frame_agregar, text="Eliminar Operador", command=eliminar_operador).grid(row=0, column=3)

tk.Label(frame_agregar, text="Pieza:").grid(row=1, column=0)
pieza_entry = tk.Entry(frame_agregar)
pieza_entry.grid(row=1, column=1)

tk.Button(frame_agregar, text="Agregar Pieza", command=agregar_pieza).grid(row=1, column=2)
tk.Button(frame_agregar, text="Eliminar Pieza", command=eliminar_pieza).grid(row=1, column=3)

# Listas de operadores y piezas
frame_listas = tk.Frame(root)
frame_listas.pack(pady=10)

operadores_listbox = tk.Listbox(frame_listas, height=5)
operadores_listbox.grid(row=0, column=0, padx=10)

piezas_listbox = tk.Listbox(frame_listas, height=5)
piezas_listbox.grid(row=0, column=1, padx=10)

# Sección de registro de tiempos
frame_registro = tk.Frame(root)
frame_registro.pack(pady=10)

operadores_seleccion = []
piezas_seleccion = []
tiempos_inicio = [None] * 10
operadores_menu = []
piezas_menu = []
botones_iniciar = []
indicadores_tiempo = []

for i in range(10):
    operador_seleccion = tk.StringVar()
    operadores_seleccion.append(operador_seleccion)
    pieza_seleccion = tk.StringVar()
    piezas_seleccion.append(pieza_seleccion)

    operadores_menu.append(tk.OptionMenu(frame_registro, operador_seleccion, ""))
    operadores_menu[i].grid(row=i, column=0)

    piezas_menu.append(tk.OptionMenu(frame_registro, pieza_seleccion, ""))
    piezas_menu[i].grid(row=i, column=1)

    btn_iniciar = tk.Button(frame_registro, text="Iniciar", command=lambda i=i: iniciar_tiempo(i))
    btn_iniciar.grid(row=i, column=2)
    botones_iniciar.append(btn_iniciar)

    tk.Button(frame_registro, text="Terminar", command=lambda i=i: terminar_tiempo(i)).grid(row=i, column=3)
    tk.Button(frame_registro, text="Borrar", command=lambda i=i: borrar_registro(i)).grid(row=i, column=4)
    
    indicador_tiempo = tk.Label(frame_registro, text="")
    indicador_tiempo.grid(row=i, column=5)
    indicadores_tiempo.append(indicador_tiempo)

# Sección de consulta de promedios
frame_consulta = tk.Frame(root)
frame_consulta.pack(pady=10)

tk.Label(frame_consulta, text="Operador:").grid(row=0, column=0)
consulta_operador = tk.StringVar()
consulta_operador_menu = tk.OptionMenu(frame_consulta, consulta_operador, "")
consulta_operador_menu.grid(row=0, column=1)

tk.Label(frame_consulta, text="Pieza:").grid(row=1, column=0)
consulta_pieza = tk.StringVar()
consulta_pieza_menu = tk.OptionMenu(frame_consulta, consulta_pieza, "")
consulta_pieza_menu.grid(row=1, column=1)

tk.Button(frame_consulta, text="Consultar Promedio", command=consultar_promedio).grid(row=2, column=0, columnspan=2)

resultado = tk.StringVar()
tk.Label(frame_consulta, textvariable=resultado).grid(row=3, column=0, columnspan=2)

actualizar_listas()

# Restaurar estado al iniciar
c.execute("SELECT operador_id, pieza_id, inicio FROM estado")
for estado in c.fetchall():
    operador_id, pieza_id, inicio = estado
    c.execute("SELECT nombre FROM operadores WHERE id=?", (operador_id,))
    operador_nombre = c.fetchone()[0]
    c.execute("SELECT nombre FROM piezas WHERE id=?", (pieza_id,))
    pieza_nombre = c.fetchone()[0]
    for i in range(10):
        if not operadores_seleccion[i].get() and not piezas_seleccion[i].get():
            operadores_seleccion[i].set(operador_nombre)
            piezas_seleccion[i].set(pieza_nombre)
            tiempos_inicio[i] = inicio
            botones_iniciar[i].config(bg="lightgreen")
            indicadores_tiempo[i].config(text="En marcha")
            break

root.mainloop()