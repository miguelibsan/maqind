import tkinter as tk
from tkinter import ttk
import time
import json
import os

class ProductionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Producción")

        # Variables
        self.operators = []
        self.pieces = []
        self.piece_assignments = {}  # {piece: [operators]}
        self.production_times = {}
        self.current_operator = tk.StringVar()
        self.current_piece = tk.StringVar()
        self.start_times = {}
        self.max_operators = 6

        # Cargar datos
        self.load_data()

        # UI Setup
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Operadores
        ttk.Label(frame, text="Operadores:").grid(row=0, column=0, sticky=tk.W)
        self.operator_combobox = ttk.Combobox(frame, textvariable=self.current_operator, values=self.operators)
        self.operator_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Agregar Operador", command=self.add_operator).grid(row=0, column=2)
        ttk.Button(frame, text="Eliminar Operador", command=self.remove_operator).grid(row=0, column=3)

        # Piezas
        ttk.Label(frame, text="Piezas:").grid(row=1, column=0, sticky=tk.W)
        self.piece_combobox = ttk.Combobox(frame, textvariable=self.current_piece, values=self.pieces)
        self.piece_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Agregar Pieza", command=self.add_piece).grid(row=1, column=2)
        ttk.Button(frame, text="Eliminar Pieza", command=self.remove_piece).grid(row=1, column=3)

        # Asignación de operadores a piezas
        self.assignment_labels = []
        self.assignment_buttons = []
        self.operator_checks = []

        for i in range(self.max_operators):
            operator_label = ttk.Label(frame, text=f"Operador {i + 1}:")
            operator_label.grid(row=2 + i, column=0, sticky=tk.W)

            check_var = tk.BooleanVar()
            check_button = ttk.Checkbutton(frame, variable=check_var)
            check_button.grid(row=2 + i, column=1, sticky=tk.W)
            self.operator_checks.append(check_var)

            self.assignment_labels.append(operator_label)
            self.assignment_buttons.append(check_button)

        ttk.Button(frame, text="Asignar Operadores", command=self.assign_operators).grid(row=8, column=0, columnspan=4, sticky=(tk.W, tk.E))

        # Botones de Producción
        self.start_buttons = []
        self.stop_buttons = []
        self.time_labels = []

        for i in range(self.max_operators):
            start_button = ttk.Button(frame, text="Iniciar Producción", command=lambda i=i: self.start_production(i))
            start_button.grid(row=9 + i, column=1, sticky=(tk.W, tk.E))
            self.start_buttons.append(start_button)

            stop_button = ttk.Button(frame, text="Terminar Producción", command=lambda i=i: self.stop_production(i), state=tk.DISABLED)
            stop_button.grid(row=9 + i, column=2, sticky=(tk.W, tk.E))
            self.stop_buttons.append(stop_button)

            time_label = ttk.Label(frame, text="")
            time_label.grid(row=9 + i, column=3, sticky=(tk.W, tk.E))
            self.time_labels.append(time_label)

        # Resultados
        ttk.Label(frame, text="Promedio por Operador y Pieza:").grid(row=15, column=0, columnspan=2, sticky=tk.W)
        self.result_label = ttk.Label(frame, text="")
        self.result_label.grid(row=15, column=2, columnspan=2, sticky=(tk.W, tk.E))
        
        # Buscar Promedio
        ttk.Label(frame, text="Buscar Promedio por Pieza:").grid(row=16, column=0, sticky=tk.W)
        self.search_piece = tk.StringVar()
        self.search_entry = ttk.Entry(frame, textvariable=self.search_piece)
        self.search_entry.grid(row=16, column=1, sticky=(tk.W, tk.E))
        self.search_result_label = ttk.Label(frame, text="")
        self.search_result_label.grid(row=16, column=2, columnspan=2, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Buscar", command=self.search_average).grid(row=16, column=3, sticky=tk.E)

    def add_operator(self):
        new_operator = self.current_operator.get()
        if new_operator and new_operator not in self.operators:
            self.operators.append(new_operator)
            self.operator_combobox['values'] = self.operators
            self.production_times[new_operator] = {}
            self.save_data()

    def remove_operator(self):
        operator = self.current_operator.get()
        if operator in self.operators:
            self.operators.remove(operator)
            self.operator_combobox['values'] = self.operators
            del self.production_times[operator]
            self.save_data()

    def add_piece(self):
        new_piece = self.current_piece.get()
        if new_piece and new_piece not in self.pieces:
            self.pieces.append(new_piece)
            self.piece_combobox['values'] = self.pieces
            self.piece_assignments[new_piece] = []
            for operator in self.operators:
                self.production_times[operator][new_piece] = []
            self.save_data()

    def remove_piece(self):
        piece = self.current_piece.get()
        if piece in self.pieces:
            self.pieces.remove(piece)
            self.piece_combobox['values'] = self.pieces
            if piece in self.piece_assignments:
                del self.piece_assignments[piece]
            for operator in self.operators:
                if piece in self.production_times[operator]:
                    del self.production_times[operator][piece]
            self.save_data()

    def assign_operators(self):
        piece = self.current_piece.get()
        if piece:
            assigned_operators = [op for op, var in zip(self.operators, self.operator_checks) if var.get()]
            self.piece_assignments[piece] = assigned_operators
            self.save_data()

    def start_production(self, operator_index):
        operator = self.operators[operator_index] if operator_index < len(self.operators) else None
        piece = self.current_piece.get()
        if operator and piece and operator in self.piece_assignments.get(piece, []):
            if operator_index not in self.start_times:
                self.start_times[operator_index] = time.time()
                self.start_buttons[operator_index]['state'] = tk.DISABLED
                self.stop_buttons[operator_index]['state'] = tk.NORMAL

    def stop_production(self, operator_index):
        operator = self.operators[operator_index] if operator_index < len(self.operators) else None
        piece = self.current_piece.get()
        if operator and piece and operator in self.start_times:
            end_time = time.time()
            elapsed_time = end_time - self.start_times[operator]
            self.production_times[operator][piece].append(elapsed_time)
            self.update_result(operator_index)
            self.save_data()
            self.start_buttons[operator_index]['state'] = tk.NORMAL
            self.stop_buttons[operator_index]['state'] = tk.DISABLED
            del self.start_times[operator]

    def update_result(self, operator_index):
        operator = self.operators[operator_index] if operator_index < len(self.operators) else None
        piece = self.current_piece.get()
        if operator and piece:
            times = self.production_times[operator][piece]
            if times:
                average_time = sum(times) / len(times)
                self.time_labels[operator_index].config(text=f"{average_time:.2f} segundos")
                self.result_label.config(text=f"{operator} - {piece}: {average_time:.2f} segundos")

    def search_average(self):
        piece = self.search_piece.get()
        total_times = []
        for operator in self.production_times:
            if piece in self.production_times[operator]:
                total_times.extend(self.production_times[operator][piece])
        if total_times:
            average_time = sum(total_times) / len(total_times)
            self.search_result_label.config(text=f"{piece}: {average_time:.2f} segundos")
        else:
            self.search_result_label.config(text="No hay datos disponibles")

    def save_data(self):
        data = {
            'operators': self.operators,
            'pieces': self.pieces,
            'piece_assignments': self.piece_assignments,
            'production_times': self.production_times
        }
        with open('production_data.json', 'w') as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists('production_data.json'):
            with open('production_data.json', 'r') as f:
                data = json.load(f)
                self.operators = data.get('operators', [])
                self.pieces = data.get('pieces', [])
                self.piece_assignments = data.get('piece_assignments', {})
                self.production_times = data.get('production_times', {})

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductionApp(root)
    root.mainloop()