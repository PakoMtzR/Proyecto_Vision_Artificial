# Proyecto Vision Artificial
---
![img1](/imgs/img_1.png)
![img2](/imgs/img_2.png)
## Descripción
Proyecto Vision Artificial es una aplicación de escritorio que ofrece una variedad de herramientas para el procesamiento y análisis de imágenes, incluyendo escaneo de documentos, aplicación de efectos visuales, OCR (reconocimiento óptico de caracteres) y esteganografía.

## Características
* **Carga de Imágenes:** Permite cargar imágenes desde el sistema de archivos.
* **Escaneo de Documentos:** Procesa la imagen para detectar y escanear documentos.
* **Rotación de Imágenes:** Opción para rotar imágenes procesadas.
* **Guardado de Imágenes:** Guarda las imágenes procesadas en formatos como PNG y JPEG.
* **Creación de PDF:** Combina múltiples imágenes escaneadas en un solo archivo PDF.
* **Reconocimiento de Caracteres (OCR):** Extrae texto de las imágenes escaneadas utilizando Tesseract OCR.
* **Aplicación de Efectos Visuales:** Aplica diversos efectos a las imágenes, como dibujo a lápiz, VHS, acuarela, caricatura, óleo, sepia, emboss, térmico, miopía, anaglyph, espejo y viñeta.
* **Esteganografía:** Permite ocultar texto dentro de una imagen y extraerlo posteriormente.
* **Interfaz de Usuario Personalizable:** Usa la biblioteca customtkinter para una apariencia moderna y personalizable.

## Requisitos
* Python 3.x
* Tesseract OCR (configurado correctamente en el sistema)
* Bibliotecas de Python:
    1. tkinter
    2. Pillow (PIL)
    3. customtkinter
    4. OpenCV (cv2)
    5. numpy
    6. pytesseract
    7. imgs_effects (biblioteca personalizada con efectos de imagen)*

## Instalacion
1. Clona este repositorio.
2. Instala las dependencias necesarias:
   ```
   pip install pillow customtkinter opencv numpy pytesseract
   ```
3. Asegúrate de tener Tesseract OCR instalado y configura la ruta en el código:
   ```
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
4. Ejecuta el programa:
   ```
   python app.py
   ```

## Uso
### Carga de Imágenes
1. Haz clic en el botón "Cargar Imagen" para seleccionar una imagen desde tu sistema de archivos.
2. La imagen seleccionada se mostrará en el área designada de la interfaz.

### Escaneo de Documentos
1. Después de cargar una imagen, haz clic en "Escanear".
2. Ajusta el umbral utilizando el deslizador para obtener el mejor resultado en blanco y negro.
3. Utiliza el botón "Rotar Imagen" si es necesario.
4. Guarda la imagen escaneada con "Guardar Imagen".

### Creación de PDF
1. Escanea y guarda las imágenes que deseas incluir en el PDF.
2. Haz clic en "Agregar" para añadir la imagen a la lista.
3. Una vez que todas las imágenes estén en la lista, haz clic en "Crear PDF" para guardarlas en un archivo PDF.

### OCR (Reconocimiento de Caracteres)
1. Carga una imagen y escanéala.
2. En la pestaña de OCR, haz clic en "Reconocer Caracteres" para extraer el texto.
3. El texto extraído se mostrará en el área de texto.
4. Usa "Limpiar" para borrar el texto o "Copiar" para copiar el texto al portapapeles.

### Aplicación de Efectos
1. En la pestaña de efectos, selecciona el efecto deseado.
2. Haz clic en el botón correspondiente al efecto para aplicarlo a la imagen.
3. Guarda la imagen con el efecto aplicado usando "Guardar Imagen".

### Esteganografía
1. En la pestaña de esteganografía, selecciona "Ocultar Texto" o "Extraer Texto".
2. Para ocultar texto, escribe el texto en el campo proporcionado y selecciona una imagen. Luego, guarda la imagen con el texto oculto.
3. Para extraer texto, selecciona la imagen que contiene el texto oculto. El texto será extraído y mostrado en el campo correspondiente.