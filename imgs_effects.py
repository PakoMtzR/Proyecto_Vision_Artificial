import cv2
import numpy as np

def sketch(img):
  # Transformamos la imagen a escala de grises
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Invertimos todos los bits de la imagen
  img_invert = cv2.bitwise_not(img_gray)

  # Hacemos un suavizado de la imagen
  img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), 0)

  # Invertimos los bits de la imagen suavizada
  img_smoothing_invert = cv2.bitwise_not(img_smoothing)

  # Generamos la imagen final
  final_img = cv2.divide(img_gray, img_smoothing_invert, scale=256)
  return final_img

def vhs(image):
  # Obtener dimensiones de la imagen
  height, width, _ = image.shape

  #
  scan_lines = np.zeros_like(image)

  n_lines = 120
  lines_value = 25
  for i in range(0, height, height//n_lines):
    scan_lines[i,:,:] = lines_value

  vhs_image = np.zeros_like(image)
  # Agregamos texto a la imagen
  cv2.putText(vhs_image, "PLAY >>", (30,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
  cv2.putText(vhs_image, "AM 08:45", (30,height-100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
  cv2.putText(vhs_image, "MAY 25 2024", (30,height-50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

  # Añadir un poco de ruido para dar un efecto más antiguo
  noise = np.random.normal(0, 15, image.shape)

  # Sumamos todas las imagenes
  vhs_image = image + noise + scan_lines

  return vhs_image

def watercolor(image):
  return cv2.stylization(image, sigma_s=60, sigma_r=0.6)

def cartoonize (image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurImage = cv2.medianBlur(image, 1)

  edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

  color = cv2.bilateralFilter(image, 9, 200, 200)

  cartoon = cv2.bitwise_and(color, color, mask = edges)

  return cartoon


def oil(image):
  return cv2.xphoto.oilPainting(image, 4, 1)

def sepia(img):
  # Crear un kernel para el efecto sepia
  sepia_filter = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])

  # Aplicamos el filtro Sepia
  sepia_img = img.dot(sepia_filter.T)

  # Nos aseguramos de que los valores estén dentro del rango [0, 255]
  sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)

  # Añadir un poco de ruido para dar un efecto más antiguo
  noise = np.random.normal(0, 25, sepia_img.shape)
  sepia_img2 = noise + sepia_img
  sepia_img2 = np.clip(sepia_img2, 0, 255).astype(np.uint8)

  return sepia_img2

def emboss(image):
  # Convertir la imagen a escala de grises
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Definir el kernel para el efecto emboss
  kernel = np.array([[ -2, -1, 0],
                    [ -1,  1, 1],
                    [  0,  1, 2]])

  # Aplicar el filtro de convolución a la imagen en escala de grises
  emboss_image = cv2.filter2D(gray_image, -1, kernel)

  # Normalizar la imagen para asegurar que los valores estén dentro del rango [0, 255]
  emboss_image = cv2.normalize(emboss_image, None, 0, 255, cv2.NORM_MINMAX)

  # Convertir la imagen de nuevo a BGR para mostrarla correctamente
  emboss_image = cv2.cvtColor(emboss_image, cv2.COLOR_GRAY2BGR)

  return emboss_image


def thermal(img):
  # Convertir la imagen a escala de grises
  gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # Aplicar un colormap para simular el efecto térmico
  # https://docs.opencv.org/4.x/d3/d50/group__imgproc__colormap.html#gga9a805d8262bcbe273f16be9ea2055a65ab3f207661ddf74511b002b1acda5ec09
  # thermal_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_TURBO)
  thermal_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_JET)
  return thermal_image

def miopia(image, ksize = (15, 15), sigmaX = 5):
  # Aplicar el filtro de desenfoque gaussiano
  # sigmaX = 5  # Desviación estándar en la dirección X
  ksize = (15, 15)  # Tamaño del kernel (debe ser impar)
  gaussian_blur = cv2.GaussianBlur(image, ksize, sigmaX)

  return gaussian_blur

def anaglyph(image, shift=10):
  # Separar los canales BGR
  b,g,r = cv2.split(image)

  # Desplazar el canal rojo a la izquierda
  r_shifted = np.roll(r, shift, axis=1)

  # Desplazar el canal cian (verde + azul) a la derecha
  b_shifted = np.roll(b, -shift, axis=1)
  g_shifted = np.roll(g, -shift, axis=1)

  # Crear la imagen Anaglifo combinando los canales desplazados
  anaglyph = cv2.merge((b_shifted, g_shifted, r_shifted))

  return anaglyph

def mirror(image):
  # Obtenemos las dimensiones de la imagen
  height, width, _ = image.shape

  # Tomamos fragmentos de la imagen
  fragmento_1 = image[:,:(width//2),:]
  fragmento_2 = image[:,(width//2):,:]

  # Concatenamos los fragmentos y los invertimos de forma estrategica
  final = np.concatenate((fragmento_2[:,::-1,:], fragmento_2, fragmento_2[:,::-1,:], fragmento_1[:,::-1,:],fragmento_1, fragmento_1[:,::-1,:]), axis=1)
  final = np.concatenate((final, final[::-1,:,:]), axis=0)

  return final

def vignette(image):
  # Obtener las dimensiones de la imagen
  rows, cols = image.shape[:2]

  # Crear una máscara de viñeta usando una matriz Gaussian
  # Puedes ajustar los parámetros sigmaX y sigmaY para cambiar la intensidad del efecto
  sigmaX = cols / 2
  sigmaY = rows / 2

  # Crear coordenadas X y Y
  X_resultant_kernel = cv2.getGaussianKernel(cols, sigmaX)
  Y_resultant_kernel = cv2.getGaussianKernel(rows, sigmaY)

  # Crear una matriz que es el producto de las dos matrices Gaussianas
  kernel = Y_resultant_kernel * X_resultant_kernel.T

  # Normalizar el kernel a un rango de 0 a 1
  mask = 255 * kernel / np.linalg.norm(kernel)
  mask = cv2.normalize(mask, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

  # Convertir la máscara a un formato de 3 canales
  mask = cv2.merge([mask, mask, mask])

  # Aplicar la máscara a la imagen
  vignette_image = np.uint8(image * mask)

  return vignette_image