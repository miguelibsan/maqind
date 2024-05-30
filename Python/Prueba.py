import tkinter as tk
from tkinter import messagebox

def calcular_precio():
    try:
        espesorpieza = float(entry_espesorpieza.get())
        diametroexteriorpieza = float(entry_diametroexteriorpieza.get())
        diametrointeriorpieza = float(entry_diametrointeriorpieza.get())
        cantidadbarrenos = float(entry_cantidadbarrenos.get() or 0)
        diametrobarrenos = float(entry_diametrobarrenos.get() or 0)
        cantidadbarrenos2 = float(entry_cantidadbarrenos2.get() or 0)
        diametrobarrenos2 = float(entry_diametrobarrenos2.get() or 0)
        cantidadchaflan = float(entry_cantidadchaflan.get() or 0)
        cantidadbisel = float(entry_cantidadbisel.get() or 0)
        largobisel = float(entry_largobisel.get() or 0)
        cantidadquintado = float(entry_cantidadquintado.get() or 0)
        
        detallado = 1.1
        gn = 1.15
        precioquintado = cantidadquintado * 5
        
        # Tabla precio corte plasma
        if (espesorpieza <= 0.5):
            preciocorteplasma = 1.5
        elif (espesorpieza <= 1.0):
            preciocorteplasma = 3.5
        elif (espesorpieza <= 1.5):
            preciocorteplasma = 5.5
        elif (espesorpieza <= 2.0):
            preciocorteplasma = 9.0
        elif (espesorpieza <= 2.5):
            preciocorteplasma = 14.0
        elif (espesorpieza <= 3.0):
            preciocorteplasma = 17.0
        elif (espesorpieza <= 3.5):
            preciocorteplasma = 33.0
        elif (espesorpieza <= 4.0):
            preciocorteplasma = 41.0
        elif (espesorpieza <= 4.5):
            preciocorteplasma = 50.0
        else:
            preciocorteplasma = 0  # Si el espesor es mayor a 4.5, no se define el precio
        
        perimetropieza = (diametroexteriorpieza * 3.1416) + (diametrointeriorpieza * 3.1416)
        
        # Tabla espesor
        if (espesorpieza <= 0.25):
            preciocorte = (perimetropieza + ((diametrobarrenos * 3.1416) * cantidadbarrenos) + ((diametrobarrenos2 * 3.1416) * cantidadbarrenos2)) * preciocorteplasma * detallado
            preciobarrenado = 0
            preciochaflan = cantidadchaflan * 10
            preciobisel = largobisel * cantidadbisel * 10
        elif (espesorpieza <= 0.75):
            preciocorte = perimetropieza * preciocorteplasma * detallado
            preciobarrenado = (cantidadbarrenos + cantidadbarrenos2) * 20
            preciochaflan = cantidadchaflan * 10
            preciobisel = largobisel * cantidadbisel * 10
        else:
            preciocorte = perimetropieza * preciocorteplasma * detallado
            preciobarrenado = ((((espesorpieza * 25) / 4.5) * 720) / 60) * (cantidadbarrenos + cantidadbarrenos2)
            preciochaflan = (((((espesorpieza * 25) / 4.5) * 720) / 60)) / 2 * cantidadchaflan
            preciobisel = largobisel * cantidadbisel * 10
        
        resultado = (preciocorte + preciobarrenado + preciochaflan + preciobisel + precioquintado) * gn
        
        label_resultado.config(text=f"{round(resultado, 2)} MXN")
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa todos los valores correctamente.")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Precio Base Plate")

tk.Label(root, text="ESPESOR DE LA PIEZA:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_espesorpieza = tk.Entry(root)
entry_espesorpieza.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="DIAMETRO EXTERIOR DE LA PIEZA:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_diametroexteriorpieza = tk.Entry(root)
entry_diametroexteriorpieza.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="DIAMETRO INTERIOR DE LA PIEZA:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_diametrointeriorpieza = tk.Entry(root)
entry_diametrointeriorpieza.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="CANTIDAD DE BARRENOS:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_cantidadbarrenos = tk.Entry(root)
entry_cantidadbarrenos.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="DIAMETRO DE BARRENOS:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_diametrobarrenos = tk.Entry(root)
entry_diametrobarrenos.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="CANTIDAD DE BARRENOS (DIFERENTES MEDIDAS):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_cantidadbarrenos2 = tk.Entry(root)
entry_cantidadbarrenos2.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="DIAMETRO DE BARRENOS (DIFERENTES MEDIDAS):").grid(row=6, column=0, padx=10, pady=5, sticky="e")
entry_diametrobarrenos2 = tk.Entry(root)
entry_diametrobarrenos2.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="CANTIDAD DE CHAFLAN:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
entry_cantidadchaflan = tk.Entry(root)
entry_cantidadchaflan.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="CANTIDAD DE BISELES:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
entry_cantidadbisel = tk.Entry(root)
entry_cantidadbisel.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="LARGO DEL BISEL:").grid(row=9, column=0, padx=10, pady=5, sticky="e")
entry_largobisel = tk.Entry(root)
entry_largobisel.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="CANTIDAD DE LETRAS:").grid(row=10, column=0, padx=10, pady=5, sticky="e")
entry_cantidadquintado = tk.Entry(root)
entry_cantidadquintado.grid(row=10, column=1, padx=10, pady=5)

tk.Button(root, text="Calcular", command=calcular_precio).grid(row=11, column=0, columnspan=2, pady=10)

label_resultado = tk.Label(root, text="0 MXN", font=("Helvetica", 16, "bold"))
label_resultado.grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()