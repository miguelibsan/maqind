import tkinter as tk
from tkinter import ttk
import pandas as pd
import time
import pickle
import os

# Inicialización de datos
operadores = []
diseños = []
registros = []

# Funciones para manejar el almacenamiento de datos
def cargar_datos():
    global operadores, diseños, registros
    if os.path.exists('datos.pkl'):
        with open('datos.pkl', 'rb') as f:
            operadores, diseños, registros = pickle.load(f)

def guardar_datos():
    with open('datos.pkl', 'wb') as f:
        pickle.dump((operadores, diseños, registros), f)

# Funciones para manejar registros
def agregar_operador():
    operador = operador_entry.get()
    if operador and operador not in operadores:
        operadores.append(operador)
        operador_entry.delete(0, tk.END)
        operador_menu['menu'].add_command(label=operador, command=tk._setit(operador_var, operador))
        calcular_menu['menu'].add_command(label=operador, command=tk._setit(calcular_operador_var, operador))
        guardar_datos()
        
def agregar_diseño():
    diseño = diseño_entry.get()
    if diseño and diseño not in diseños:
        diseños.append(diseño)
        diseño_entry.delete(0, tk.END)
        diseño_menu['menu'].add_command(label=diseño, command=tk._setit(diseño_var, diseño))
        calcular_diseño_menu['menu'].add_command(label=diseño, command=tk._setit(calcular_diseño_var, diseño))
        guardar_datos()

def iniciar_tiempo(index):
    global start_times
    start_times[index] = time.time()
    status_labels[index].config(text="El tiempo está corriendo...")

def terminar_tiempo(index):
    end_time = time.time()
    elapsed_time = end_time - start_times[index]
    registros.append({
        'Operador': operador_vars[index].get(),
        'Diseño': diseño_vars[index].get(),
        'Tiempo': elapsed_time
    })
    status_labels[index].config(text="Registro guardado.")
    guardar_datos()

def mostrar_promedios():
    operador = calcular_operador_var.get()
    diseño = calcular_diseño_var.get()
    
    df = pd.DataFrame(registros)
    if not df.empty:
        if operador:
            df_operador = df[df['Operador'] == operador]
            promedio_operador = df_operador['Tiempo'].mean()
            promedio_label.config(text=f"Promedio de tiempo para {operador}: {promedio_operador:.2f} segundos")
        
        if diseño:
            df_diseño = df[df['Diseño'] == diseño]
            promedio_diseño = df_diseño['Tiempo'].mean()
            promedio_label.config(text=f"Promedio de tiempo para {diseño}: {promedio_diseño:.2f} segundos")

def buscar_diseño(event, index):
    search_text = event.widget.get()
    matching_diseños = [diseño for diseño in diseños if search_text.lower() in diseño.lower()]
    diseño_menu_vars[index]['menu'].delete(0, 'end')
    for diseño in matching_diseños:
        diseño_menu_vars[index]['menu'].add_command(label=diseño, command=tk._setit(diseño_vars[index], diseño))

# Creación de la ventana principal
root = tk.Tk()
root.title("Registro de Tiempos de Operadores")

# Cargar datos guardados
cargar_datos()

# Sección de registros
registros_frame = ttk.LabelFrame(root, text="Registros")
registros_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(registros_frame, text="Operador:").grid(row=0, column=0)
operador_entry = tk.Entry(registros_frame)
operador_entry.grid(row=0, column=1)
tk.Button(registros_frame, text="Agregar Operador", command=agregar_operador).grid(row=0, column=2)

tk.Label(registros_frame, text="Diseño:").grid(row=1, column=0)
diseño_entry = tk.Entry(registros_frame)
diseño_entry.grid(row=1, column=1)
tk.Button(registros_frame, text="Agregar Diseño", command=agregar_diseño).grid(row=1, column=2)

# Sección de menú de selección
seleccion_frame = ttk.LabelFrame(root, text="Selección")
seleccion_frame.grid(row=1, column=0, padx=10, pady=10)

operador_vars = []
diseño_vars = []
diseño_search_entries = []
diseño_menu_vars = []
status_labels = []
start_times = [None] * 10

for i in range(10):
    operador_var = tk.StringVar()
    operador_vars.append(operador_var)
    operador_menu = ttk.OptionMenu(seleccion_frame, operador_var, "Selecciona un Operador", *operadores)
    operador_menu.grid(row=i, column=0)
    
    diseño_var = tk.StringVar()
    diseño_vars.append(diseño_var)
    diseño_search_entry = tk.Entry(seleccion_frame)
    diseño_search_entry.grid(row=i, column=1)
    diseño_search_entry.bind("<KeyRelease>", lambda event, index=i: buscar_diseño(event, index))
    diseño_search_entries.append(diseño_search_entry)
    
    diseño_menu_var = ttk.OptionMenu(seleccion_frame, diseño_var, "Selecciona un Diseño")
    diseño_menu_var.grid(row=i, column=2)
    diseño_menu_vars.append(diseño_menu_var)

    tk.Button(seleccion_frame, text="Iniciar", command=lambda index=i: iniciar_tiempo(index)).grid(row=i, column=3)
    tk.Button(seleccion_frame, text="Terminar", command=lambda index=i: terminar_tiempo(index)).grid(row=i, column=4)

    status_label = tk.Label(seleccion_frame, text="")
    status_label.grid(row=i, column=5)
    status_labels.append(status_label)

# Sección de promedios
calcular_frame = ttk.LabelFrame(root, text="Calcular Promedios")
calcular_frame.grid(row=2, column=0, padx=10, pady=10)

calcular_operador_var = tk.StringVar()
calcular_menu = ttk.OptionMenu(calcular_frame, calcular_operador_var, "Selecciona un Operador", *operadores)
calcular_menu.grid(row=0, column=0)

calcular_diseño_var = tk.StringVar()
calcular_diseño_menu = ttk.OptionMenu(calcular_frame, calcular_diseño_var, "Selecciona un Diseño", *diseños)
calcular_diseño_menu.grid(row=0, column=1)

tk.Button(calcular_frame, text="Mostrar Promedios", command=mostrar_promedios).grid(row=0, column=2)

promedio_label = tk.Label(calcular_frame, text="")
promedio_label.grid(row=1, column=0, columnspan=3)

root.mainloop()