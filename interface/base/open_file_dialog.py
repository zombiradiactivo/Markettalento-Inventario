import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    """Abre el explorador de archivos y retorna la ruta seleccionada"""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Seleccionar base de datos",
        filetypes=[("SQLite Database", "*.db"), ("Todos los archivos", "*.*")]
    )
    root.destroy()
    return file_path

