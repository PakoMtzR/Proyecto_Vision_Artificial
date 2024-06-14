import tkinter as tk
from tkinter import ttk
import os

# https://github.com/rdbende/Azure-ttk-theme
def set_azure_theme(root):
    theme_path = os.path.join(os.path.dirname(__file__), 'Azure-Theme', 'azure.tcl')
    # theme_path = os.path.join(os.path.dirname(__file__), 'Sun-Valley-Theme', 'sv_ttk', 'sv.tcl')
    
    root.tk.call('source', theme_path)
    root.tk.call('set_theme', 'dark')  # Configuramos el tema

def add_to_listbox():
    # Obtener el valor del Entry
    value = entry.get()
    # Verificar que el valor no sea nulo
    if value:
        # Agregar el valor al Listbox
        listbox.insert(tk.END, value)
        # Limpiar el Entry después de agregar el valor
        entry.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación con Azure Ttk Theme")

# Aplicar el tema Azure
set_azure_theme(root)

# Crear un widget de ejemplo
label = ttk.Label(root, text="Hola, Azure Ttk Theme!")
label.pack(padx=20, pady=20)

# Crear un Entry
entry = ttk.Entry(root)
entry.pack(padx=20, pady=20)

# Crear un botón y vincularlo a la función add_to_listbox
button = ttk.Button(root, text="Agregar", command=add_to_listbox)
button.pack(padx=20, pady=20)

# Crear un Listbox
listbox = tk.Listbox(root)
listbox.pack(padx=20, pady=20)

# Iniciar el bucle principal de la aplicación
root.mainloop()
