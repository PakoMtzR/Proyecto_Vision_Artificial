import tkinter as tk
from tkinter import ttk
import os

def set_azure_theme(root):
    theme_path = os.path.join(os.path.dirname(__file__), 'Azure-Theme', 'azure.tcl')
    # theme_path = os.path.join(os.path.dirname(__file__), 'Sun-Valley-Theme', 'sv_ttk', 'sv.tcl')
    
    root.tk.call('source', theme_path)
    root.tk.call('set_theme', 'dark')  # Configuramos el tema


# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación con Azure Ttk Theme")

# Aplicar el tema Azure
set_azure_theme(root)

# Crear un widget de ejemplo
label = ttk.Label(root, text="Hola, Azure Ttk Theme!")
label.pack(padx=20, pady=20)

button = ttk.Button(root, text="Haz clic aquí")
button.pack(padx=20, pady=20)

list_box = ttk.Spinbox(root, from_=0, to=100)
list_box.pack(padx=20, pady=20)

combobox = ttk.Combobox(root, values=["hola"])
combobox.pack(padx=20, pady=20)

# Iniciar el bucle principal de la aplicación
root.mainloop()
