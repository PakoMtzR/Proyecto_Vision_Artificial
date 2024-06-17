import cv2
import numpy as np

def ordenar_puntos(self, puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()
    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1])
    x1_order = y_order[:2]
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])
    x2_order = y_order[2:4]
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])
    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]


image = cv2.imread(r"imgs/Doc1.jpg")

max_dim = 750
height, width = image.shape[:2]
scale = max_dim / max(height, width)
image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, img_bw = cv2.threshold(gray_blur, 125, 255, cv2.THRESH_BINARY)
canny = cv2.Canny(img_bw, 10, 150)

contours = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

height, width = gray.shape

for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    print(f"{len(approx)} puntos encontrados")  # para verificar cuanto puntos encontro

    if len(approx) == 4:
        puntos = ordenar_puntos(approx)
        points_1 = np.float32(puntos)
        points_2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(points_1, points_2)
        image = cv2.warpPerspective(gray, matrix, (width, height))

        _, image_bw = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)


cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()