import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import cv2
import numpy as np
import pytesseract
import imgs_effects

# Ruta al ejecutable de Tesseract (cambia esto según tu instalación)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Modificando la apariencia
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    APP_NAME = "Document Scanner"
    WIDTH = 850
    HEIGHT = 700

    # Funcion __init__ crea la ventana y los elementos de la interfaz
    def __init__(self):
        super().__init__()
        # Creamos las imagenes con valor nulo
        self.image = None
        self.processed_image = None
        self.image_with_effect = None
        self.images2pdf = []
        self.image_counter = 0

        # Solo esta este boton para cerrar la ventana en lo que la interfaz esta en desarrollo
        self.bind("<Return>", lambda event: self.destroy())

        # Configuracion de la pantalla
        # ---------------------------------------------------------------------
        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # ---------------------------------------------------------------------

        # Definimos los frames
        # ---------------------------------------------------------------------
        self.img_frame = ctk.CTkFrame(master=self, corner_radius=0)     # Frame donde colocaremos la imagen
        self.img_frame.grid(row=0, column=0, sticky="nesw")
        self.options_frame = ctk.CTkFrame(master=self, corner_radius=0) # Frame donde estaran las opciones para
        self.options_frame.grid(row=0, column=1, sticky="nesw")         # mofidicar la imagen
        # ---------------------------------------------------------------------

        # Elementos dentro de img_frame
        # ---------------------------------------------------------------------
        self.btn_load_img = ctk.CTkButton(master=self.img_frame, text="Cargar Imagen", command=self.upload_image)
        self.btn_load_img.pack(pady=(30,10), padx=10)
        self.image_label = ctk.CTkLabel(master=self.img_frame, text="No image selected")
        self.image_label.pack(pady=10, padx=10, expand=True)
        # ---------------------------------------------------------------------

        # Elementos dentro de options_frame
        # ---------------------------------------------------------------------
        self.tabview = ctk.CTkTabview(master=self.options_frame)
        self.tabview.pack(pady=10, padx=10, expand=True, fill="both") # 
        self.tabview.add("tab 1")
        self.tabview.add("tab 2")
        self.tabview.add("tab 3")
        self.tabview.set("tab 1")
        
        # Elementos dentro de Tab1
        self.btn_scan_img = ctk.CTkButton(master=self.tabview.tab("tab 1"), text="Escanear", command=self.scan_image)
        self.btn_scan_img.pack(pady=10, padx=10)
        self.threshold_slider = ctk.CTkSlider(master=self.tabview.tab("tab 1"), from_=0, to=255, command=self.slider_callback)
        self.threshold_slider.pack(pady=10, padx=10) #, fill=tk.BOTH
        self.btn_rotate_img = ctk.CTkButton(master=self.tabview.tab("tab 1"), text="Rotar Imagen", command=self.rotate_image)
        self.btn_rotate_img.pack(pady=10, padx=10)
        self.btn_save_img = ctk.CTkButton(master=self.tabview.tab("tab 1"), text="Guardar Imagen", command=self.save_image)
        self.btn_save_img.pack(pady=10, padx=10)
        self.label_list = ctk.CTkLabel(master=self.tabview.tab("tab 1"), text="Lista de Imagenes")
        self.label_list.pack(pady=2, padx=10)
        self.list_img = ctk.CTkScrollableFrame(master=self.tabview.tab("tab 1"))
        self.list_img.pack(pady=10, padx=25, fill="both", expand=True)
        self.btn_add2list = ctk.CTkButton(master=self.tabview.tab("tab 1"), text="Agregar", command=self.add_images2pdf_list)
        self.btn_add2list.pack(pady=10, padx=10)
        self.btn_create_pdf = ctk.CTkButton(master=self.tabview.tab("tab 1"), text="Crear PDF", command=self.save_pdf)
        self.btn_create_pdf.pack(pady=10, padx=10)

        # Elementos dentro de Tab 2
        self.btn_ocr = ctk.CTkButton(master=self.tabview.tab("tab 2"), text="Reconocer Caracteres", command=self.ocr)
        self.btn_ocr.pack(pady=10, padx=10)
        self.textbox = ctk.CTkTextbox(master=self.tabview.tab("tab 2"))
        self.textbox.pack(pady=10, padx=10, fill="both", expand=True)
        self.btn_clean = ctk.CTkButton(master=self.tabview.tab("tab 2"), text="Limpiar", command=self.clean_textbox)
        self.btn_clean.pack(pady=10, padx=10)
        self.btn_copy = ctk.CTkButton(master=self.tabview.tab("tab 2"), text="Copiar", command=self.copy_textbox)
        self.btn_copy.pack(pady=10, padx=10)

        # Elementos dentro de Tab 3
        btns = ["Dibujo Lapiz", "VHS", "Sepia"]
        for i, text_btn in enumerate(btns):
            self.btn = ctk.CTkButton(master=self.tabview.tab("tab 3"), text=text_btn, command=self.apply_effect(i))
            self.btn.pack(pady=10, padx=10)
        # ---------------------------------------------------------------------

    # Funcion para cargar la imagen a la interfaz
    def upload_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if filepath:
            self.image = cv2.imread(filepath)
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.update_image(image_rgb)

    # Funcion que permite rotar la imagen procesada
    def rotate_image(self):
        if self.processed_image is None:
            return
        
        self.processed_image = cv2.rotate(self.processed_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.update_image(self.processed_image)
        return

    # Funcion para poder guardar la imagen procesada en un directorio
    def save_image(self):
        if self.processed_image is None:
            return
        
        # cv2.imwrite("img1.jpg", self.image)
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if filepath:
            pil_image = Image.fromarray(self.processed_image)
            pil_image.save(filepath)
            self.mostrar_advertencia("Guardado", "La imagen ha sido guardada exitosamente")

    # Funcion para escalar la imagen para que se pueda visualizar en la interfaz
    def resize_image(self, image, max_dim = 750):   # 750 630
        height, width = image.shape[:2]
        scale = max_dim / max(height, width)
        return cv2.resize(image, (0, 0), fx=scale, fy=scale)

    # Funcion para poder actulizar la imagen en la interfaz
    def update_image(self, image_array):
        resized_image_array = self.resize_image(image_array)
        pil_image = Image.fromarray(resized_image_array)
        ctk_image = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=ctk_image, text="")
        self.image_label.image = ctk_image  # Guardar referencia a la imagen

    # Funcion para cambiar el umbral y procesar la imagen blanco y negro en tiempo real
    def slider_callback(self, value):
        if self.processed_image is None:
            return
        
        slider_value = int(value)
        # gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, image_bw = cv2.threshold(self.image, slider_value, 255, cv2.THRESH_BINARY)
        self.processed_image = image_bw
        self.update_image(image_bw)

    # Funcion para escanear el documento dentro de la imagen
    # Reconocimiento de bordes, transformacion y umbralicilizacion
    def scan_image(self):
        if self.image is None:
            self.mostrar_advertencia("ERROR", "Primero carga una imagen")
            return
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 10, 150)
        canny = cv2.dilate(canny, None, iterations=1)

        # gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # _, img_bw = cv2.threshold(gray_blur, 125, 255, cv2.THRESH_BINARY)
        # canny = cv2.Canny(img_bw, 10, 150)

        contours = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        height, width = gray.shape

        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            print(f"{len(approx)} puntos encontrados")  # para verificar cuanto puntos encontro

            if len(approx) == 4:
                puntos = self.ordenar_puntos(approx)
                points_1 = np.float32(puntos)
                points_2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                matrix = cv2.getPerspectiveTransform(points_1, points_2)
                self.image = cv2.warpPerspective(gray, matrix, (width, height))

                _, image_bw = cv2.threshold(self.image, 125, 255, cv2.THRESH_BINARY)
                self.processed_image = image_bw
                self.update_image(image_bw)
                return

        self.mostrar_advertencia("Error", "No se pudo encontrar un documento en la imagen")
    
    # Funcion que agrega la imagen a la lista para poder crear el pdf
    def add_images2pdf_list(self):
        if self.processed_image is None:
            return
        
        self.images2pdf.append(self.processed_image)
        label = ctk.CTkLabel(master=self.list_img, text=f"Imagen_{self.image_counter}")
        label.pack(pady=5, padx=2)
        self.image_counter += 1

    # Funcion que toma todas las imagenes agregadas de la lista para generar un pdf
    def save_pdf(self):
        # if self.images2pdf == []:
        if not self.images2pdf:
            self.mostrar_advertencia("Error", "No hay imagen procesada para guardar como PDF")
            return

        # Guardamos la lista de imagenes en un pdf
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filepath:
            pil_images = [Image.fromarray(img).convert("RGB") for img in self.images2pdf]
            pil_images[0].save(filepath, save_all=True, append_images=pil_images[1:], resolution=100.0)
            self.mostrar_advertencia("Guardado", "El PDF ha sido guardado exitosamente")
        
        # Limpiamos la lista de imagenes, los elementos dentro del CTkScrollableFrame y reiniciamos el contador
        # self.images2pdf = []
        self.images2pdf.clear()
        self.image_counter = 0
        for label in self.list_img.winfo_children():
            label.destroy()
    
    def ocr(self):
        self.scan_image()
        text = pytesseract.image_to_string(self.processed_image)
        self.textbox.delete("0.0", tk.END)
        self.textbox.insert("0.0", text)
            
    def clean_textbox(self):
        self.textbox.delete("0.0", ctk.END)
    
    def copy_textbox(self):
        self.clipboard_clear()    
        self.clipboard_append(self.textbox.get("0.0", ctk.END).strip())                     

    def apply_effect(self, effect):
        if self.image == None:
            return
        
        match(effect):
            case 0:
                self.image_with_effect = imgs_effects.sketch(self.image)
            case 1:
                self.image_with_effect = imgs_effects.vhs(self.image)
            case 2:
                self.image_with_effect = imgs_effects.sepia(self.image)
            case _:
                print("No existe ese efecto")

        self.update_image(self.image_with_effect)

    # Funcion para poder enviar avisos o advertencias dentro de la interfaz
    def mostrar_advertencia(self, title, message):
        # Configuracion de ventana
        advertencia_ventana = ctk.CTkToplevel(self)
        advertencia_ventana.title(title)
        advertencia_ventana.geometry("350x150")
        advertencia_ventana.grab_set()  # Hace que solo se pueda interactuar con esta ventana hasta que se cierre

        # Elementos dentro de la ventana
        frame = ctk.CTkFrame(master=advertencia_ventana)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        label = ctk.CTkLabel(master=frame, text=message)
        label.pack(pady=10, padx=10)
        button = ctk.CTkButton(master=frame, text="Cerrar", command=advertencia_ventana.destroy)
        button.pack(pady=10, padx=10)

        # Vincular la tecla Enter a la función de cierre de la ventana de advertencia
        advertencia_ventana.bind("<Return>", lambda event: advertencia_ventana.destroy())
    
    # Funcion para ordenar los puntos para poder realizar la transformacion del documento una vez que reconocimos los bordes
    def ordenar_puntos(self, puntos):
        n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
        y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])
        x1_order = y_order[:2]
        x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
        x2_order = y_order[2:4]
        x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])
        return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

if __name__ == "__main__":
    app = App()
    app.mainloop()
