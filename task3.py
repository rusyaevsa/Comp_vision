import cv2

# открываем и ресайзим изображение
img = cv2.imread("pic/ocean.jpg", cv2.IMREAD_UNCHANGED)
img = cv2.resize(img, (640, 420))
# переводим в оттенки сеерого
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Before", img)
cv2.imshow("Gray", gray)

# создание выравнивания гистограмм
img_eh = cv2.equalizeHist(gray)
cv2.imshow('equalizeHist', img_eh)

# локальное выравнивание гистограмм
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
dst = clahe.apply(gray)
cv2.imshow("Local", dst)

# Гауссовское размытие
hsv = cv2.GaussianBlur(gray, (9, 9), 0)
cv2.imshow('Gaussian Blur', hsv)

# фильтр Лапласа
laplacian = cv2.Laplacian(hsv, cv2.CV_64F)

# фильтры Собеля
sobelx = cv2.Sobel(hsv, cv2.CV_64F, 1, 0, ksize=1) # x
sobely = cv2.Sobel(hsv, cv2.CV_64F, 0, 1, ksize=5) # y
sobelxy = cv2.Sobel(hsv, cv2.CV_64F, 1, 1, ksize=5) # y
cv2.imshow('Laplacian', laplacian)
cv2.imshow('Sobel x', sobelx)
cv2.imshow('Sobel y', sobely)
cv2.imshow('Sobel xy', sobelxy)

# открываем изображение с собакой
img2 = cv2.imread("pic/haska.png", cv2.IMREAD_UNCHANGED)
img2 = cv2.resize(img2, (300, 300))

# извлекаем размеры изображений
h, w, _ = img2.shape
rows, cols, _ = img.shape

# позиция изображения на переднем плане
y, x = 100, 100

# выполняем цикл по всем пикселям для смешивания изображений
for i in range(h):
    for j in range(w):
        if x + i >=  rows or y + j >=  cols:
            continue
        # считываем альфа-канал
        alpha = float(img2[i][j][3] / 255.0)
        img[x + i][y + j] = alpha * img2[i][j][:3] + (1 - alpha) * img[x + i][y + j]

cv2.imshow('Alpha', img)
cv2.waitKey(0)