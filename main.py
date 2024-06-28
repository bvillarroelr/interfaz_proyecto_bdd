import tkinter as tk
from tkinter import messagebox
import sqlite3

class ColegioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Escolar")

        self.conn = sqlite3.connect('colegio.db')
        self.cursor = self.conn.cursor()

        self.crear_inicio()

    def crear_inicio(self):
        self.limpiar_ventana()

        btn_estudiante = tk.Button(self.root, text="Vista Estudiante", command=self.mostrar_calificaciones)
        btn_estudiante.pack(pady=10)
        
        btn_apoderado = tk.Button(self.root, text="Vista Apoderado", command=self.mostrar_calificaciones)
        btn_apoderado.pack(pady=10)
        
        btn_profesor = tk.Button(self.root, text="Vista Profesor", command=self.menu_profesor)
        btn_profesor.pack(pady=10)

    def mostrar_calificaciones(self):
        self.limpiar_ventana()

        self.cursor.execute("SELECT usuarios.nombre, calificaciones.materia, calificaciones.calificacion FROM calificaciones JOIN usuarios ON calificaciones.estudiante_id = usuarios.id")
        calificaciones = self.cursor.fetchall()

        if calificaciones:
            for nombre, materia, calificacion in calificaciones:
                label = tk.Label(self.root, text=f"{nombre} - {materia}: {calificacion}")
                label.pack()
        else:
            label = tk.Label(self.root, text="No hay calificaciones disponibles")
            label.pack()

        btn_volver = tk.Button(self.root, text="Volver", command=self.crear_inicio)
        btn_volver.pack(pady=10)

    def menu_profesor(self):
        self.limpiar_ventana()

        btn_ver_calificaciones = tk.Button(self.root, text="Ver Calificaciones", command=self.mostrar_calificaciones_profesor)
        btn_ver_calificaciones.pack(pady=10)
        
        btn_agregar_calificacion = tk.Button(self.root, text="Agregar Calificación", command=self.agregar_calificacion)
        btn_agregar_calificacion.pack(pady=10)

        btn_volver = tk.Button(self.root, text="Volver", command=self.crear_inicio)
        btn_volver.pack(pady=10)

    def mostrar_calificaciones_profesor(self):
        self.limpiar_ventana()

        self.cursor.execute("SELECT usuarios.nombre, calificaciones.materia, calificaciones.calificacion FROM calificaciones JOIN usuarios ON calificaciones.estudiante_id = usuarios.id")
        calificaciones = self.cursor.fetchall()

        if calificaciones:
            for nombre, materia, calificacion in calificaciones:
                label = tk.Label(self.root, text=f"{nombre} - {materia}: {calificacion}")
                label.pack()
        else:
            label = tk.Label(self.root, text="No hay calificaciones disponibles")
            label.pack()

        btn_volver = tk.Button(self.root, text="Volver", command=self.menu_profesor)
        btn_volver.pack(pady=10)

    def agregar_calificacion(self):
        self.limpiar_ventana()

        label_estudiante = tk.Label(self.root, text="Nombre del Estudiante")
        label_estudiante.pack()
        self.entry_estudiante = tk.Entry(self.root)
        self.entry_estudiante.pack()

        label_materia = tk.Label(self.root, text="Materia")
        label_materia.pack()
        self.entry_materia = tk.Entry(self.root)
        self.entry_materia.pack()

        label_calificacion = tk.Label(self.root, text="Calificación")
        label_calificacion.pack()
        self.entry_calificacion = tk.Entry(self.root)
        self.entry_calificacion.pack()

        btn_guardar = tk.Button(self.root, text="Guardar", command=self.guardar_calificacion)
        btn_guardar.pack(pady=10)

        btn_volver = tk.Button(self.root, text="Volver", command=self.menu_profesor)
        btn_volver.pack(pady=10)

    def guardar_calificacion(self):
        estudiante = self.entry_estudiante.get()
        materia = self.entry_materia.get()
        calificacion = float(self.entry_calificacion.get())

        self.cursor.execute("SELECT id FROM usuarios WHERE nombre=? AND rol='Estudiante'", (estudiante,))
        estudiante_id = self.cursor.fetchone()

        if estudiante_id:
            estudiante_id = estudiante_id[0]
            self.cursor.execute("INSERT INTO calificaciones (estudiante_id, materia, calificacion) VALUES (?, ?, ?)",
                                (estudiante_id, materia, calificacion))
            self.conn.commit()
            messagebox.showinfo("Información", "Calificación guardada correctamente")
        else:
            messagebox.showerror("Error", "Estudiante no encontrado")

        self.menu_profesor()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColegioApp(root)
    root.mainloop()
