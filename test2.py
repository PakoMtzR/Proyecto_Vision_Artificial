import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import cv2
import numpy as np

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    APP_NAME = "Document Scanner"
    WIDTH = 850
    HEIGHT = 700

    def __init__(self):
        super().__init__()
        self.image = None

        # Configure window
        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)

        # Configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Definimos los frames
        self.img_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.img_frame.grid(row=0, column=0, sticky="nesw")
        self.options_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.options_frame.grid(row=0, column=1, sticky="nesw")

        # Elementos dentro de img_frame
        self.image_label = ctk.CTkLabel(master=self.img_frame, text="No image selected")
        self.image_label.pack(pady=(30,5), padx=10)
        self.threshold_slider = ctk.CTkSlider(master=self.img_frame, from_=0, to=255, command=self.slider_callback)
        self.threshold_slider.pack(pady=10, padx=50) #, fill=tk.BOTH
        self.btn_load_img = ctk.CTkButton(master=self.img_frame, text="Cargar Imagen", command=self.cargar_imagen)
        self.btn_load_img.pack(pady=5, padx=10)
        self.btn_scan_img = ctk.CTkButton(master=self.img_frame, text="Escanear", command=self.escanear_imagen)
        self.btn_scan_img.pack(pady=5, padx=10)

        # Elementos dentro de options_frame

        # Elementos dentro de pdf_frame
        self.list_img = ctk.CTkScrollableFrame(master=self.options_frame)
        self.list_img.pack(pady=10, padx=10, fill="both", expand=True)
        self.btn_save_img = ctk.CTkButton(master=self.options_frame, text="Guardar Imagen")
        self.btn_save_img.pack(pady=10, padx=10)
        self.btn_create_pdf = ctk.CTkButton(master=self.options_frame, text="Crear PDF")
        self.btn_create_pdf.pack(pady=10, padx=10)

    def slider_callback(self, value):
        if self.image is None:
            return

        slider_value = int(value)
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, image_bw = cv2.threshold(gray_image, slider_value, 255, cv2.THRESH_BINARY)
        self.update_image(image_bw)

    def cargar_imagen(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if filepath:
            self.image = cv2.imread(filepath)
            self.image = self.resize_image(self.image)
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.update_image(image_rgb)

    def escanear_imagen(self):
        if self.image is None:
            self.mostrar_advertencia("ERROR: ALVTO2", "Tonto, primero carga una imagen")
            return
        
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, img_bw = cv2.threshold(gray_blur, 125, 255, cv2.THRESH_BINARY)
        canny = cv2.Canny(img_bw, 10, 150)

        cv2.imshow("gray", gray)
        cv2.imshow("gray_blur", gray_blur)
        cv2.imshow("img_bw", img_bw)
        cv2.imshow("canny", canny)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        contours = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        height, width = gray.shape

        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            print(len(approx))  # para verificar cuanto puntos encontro

            if len(approx) == 4:
                puntos = self.ordenar_puntos(approx)
                points_1 = np.float32(puntos)
                points_2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                matrix = cv2.getPerspectiveTransform(points_1, points_2)
                self.image = cv2.warpPerspective(gray, matrix, (width, height))

                _, image_bw = cv2.threshold(self.image, 125, 255, cv2.THRESH_BINARY)
                self.update_image(image_bw)
                return

        self.mostrar_advertencia("Error", "No se encontró un documento en la imagen")
    
    def resize_image(self, image, max_dim = 680):
        height, width, _ = image.shape
        scale = max_dim / max(height, width)
        return cv2.resize(image, (0, 0), fx=scale, fy=scale)

    def update_image(self, image_array):
        pil_image = Image.fromarray(image_array)
        ctk_image = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=ctk_image, text="")
        self.image_label.image = ctk_image  # Guardar referencia a la imagen

    def ordenar_puntos(self, puntos):
        n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
        y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])
        x1_order = y_order[:2]
        x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
        x2_order = y_order[2:4]
        x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])
        return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

    def mostrar_advertencia(self, title, message):
        advertencia_ventana = ctk.CTkToplevel(self)
        advertencia_ventana.title(title)
        advertencia_ventana.geometry("300x150")
        advertencia_ventana.grab_set()

        frame = ctk.CTkFrame(master=advertencia_ventana)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        label = ctk.CTkLabel(master=frame, text=message)
        label.pack(pady=10, padx=10)

        button = ctk.CTkButton(master=frame, text="Cerrar", command=advertencia_ventana.destroy)
        button.pack(pady=10, padx=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
