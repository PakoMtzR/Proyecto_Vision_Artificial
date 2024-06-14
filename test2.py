import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import cv2
import numpy as np

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    APP_NAME = "Todavia no tengo el nombre"
    WIDTH = 850
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        # Configure window
        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)

        # Configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Definimos los frames
        self.img_frame = ctk.CTkFrame(master=self)
        self.img_frame.grid(row=0, column=0, sticky="nesw")
        self.options_frame = ctk.CTkFrame(master=self)
        self.options_frame.grid(row=0, column=1, sticky="nesw")
        self.pdf_frame = ctk.CTkFrame(master=self)
        self.pdf_frame.grid(row=0, column=2, sticky="nesw")

        # Elementos dentro de img_frame
        self.image_label = ctk.CTkLabel(master=self.img_frame, text="No image selected")
        self.image_label.pack(pady=10, padx=10)
        self.threshold_scale = ctk.CTkSlider(master=self.img_frame)
        self.threshold_scale.pack(pady=10, padx=10)

        # Elementos dentro de options_frame
        self.btn_load_img = ctk.CTkButton(master=self.options_frame, text="Cargar Imagen", command=self.cargar_imagen)
        self.btn_load_img.pack(pady=10, padx=10)
        self.btn_scan_img = ctk.CTkButton(master=self.options_frame, text="Escanear")
        self.btn_scan_img.pack(pady=10, padx=10)
        self.btn_save_img = ctk.CTkButton(master=self.options_frame, text="Guardar Imagen")
        self.btn_save_img.pack(pady=10, padx=10)

        # Elementos dentro de pdf_frame
        self.list_img = ctk.CTkScrollableFrame(master=self.pdf_frame)
        self.list_img.pack(pady=10, padx=10, fill="both", expand=True)
        self.btn_create_pdf = ctk.CTkButton(master=self.pdf_frame, text="Crear PDF")
        self.btn_create_pdf.pack(pady=10, padx=10)

    def cargar_imagen(self):
        # Abrir el diálogo de selección de archivos
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if filepath:
            # Cargar la imagen seleccionada con OpenCV
            image = cv2.imread(filepath)
            
            # Convertir la imagen de BGR a RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Convertir la imagen a PIL
            pil_image = Image.fromarray(image)
            
            # Redimensionar la imagen para ajustar al label
            pil_image = pil_image.resize((200, 200), Image.Resampling.LANCZOS)
            
            # Convertir la imagen PIL a un objeto ImageTk
            ctk_image = ImageTk.PhotoImage(pil_image)
            
            # Actualizar la etiqueta con la nueva imagen
            self.image_label.configure(image=ctk_image, text="")
            self.image_label.image = ctk_image  # Guardar referencia a la imagen


if __name__ == "__main__":
    app = App()
    app.mainloop()
