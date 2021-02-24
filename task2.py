import cv2
import numpy

img = cv2.imread("pic/tuman.jpg")
img = cv2.resize(img, (640, 420))
cv2.imshow('Before', img)

# переводим изображение в LAB
img_temp = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# делаем массив из картинки
img_new = numpy.array(img_temp, dtype = numpy.float32)

# вычленяем наибольшее и наименьшее значение параметра L
max_l, min_l = img_new[:, :, 0].max(), img_new[:, :, 0].min()

# масштабируем параметр L на интервал 0...255
img_new[:, :, 0] = 255 * (img_new[:, :, 0] - min_l) / (max_l - min_l)

img_new = numpy.array(img_new, dtype = numpy.uint8)

# переводим изображение назад в BGR
img_res = cv2.cvtColor(img_new, cv2.COLOR_LAB2BGR)

# выводим результат
cv2.imshow('LAB', img_res)

cv2.waitKey(0)