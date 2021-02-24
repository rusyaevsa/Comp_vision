import cv2
import numpy as np

img1 = cv2.imread("pic/pizza.jpg")
img1 = cv2.resize(img1, (400, 400))
cv2.imshow("Pizza1", img1)
img2 = cv2.imread("pic/pizza2.jpg")
img2 = cv2.resize(img2, (400, 400))
cv2.imshow("Pizza2", img2)
_, width, _ = img1.shape
width_2 = width // 2
# просто соеденяем две половинки у картинок
just_blend = np.hstack((img1[:, :width_2], img2[:, width_2:]))

# Пирамиды Гаусса для изображений
img_down = img1.copy()
img_down2 = img2.copy()
gauss = [img_down]
gauss2 = [img_down2]
for i in range(6):
    img_down = cv2.pyrDown(img_down)
    gauss.append(img_down)
    img_down2 = cv2.pyrDown(img_down2)
    gauss2.append(img_down2)

# Пирамиды Лапласа для изображений
layer = gauss[5]
laplacian = [layer]
layer2 = gauss2[5]
laplacian2 = [layer2]
for i in range(5, 0, -1):
    size = (gauss[i - 1].shape[1], gauss[i - 1].shape[0])
    gauss_expanded = cv2.pyrUp(gauss[i], dstsize=size)
    lap_sub = cv2.subtract(gauss[i - 1], gauss_expanded)
    laplacian.append(lap_sub)
    gauss_expanded2 = cv2.pyrUp(gauss2[i], dstsize=size)
    lap_sub2 = cv2.subtract(gauss2[i - 1], gauss_expanded2)
    laplacian2.append(lap_sub2)

# соединяем пирамиды Лапласа по вертикали
blend = []
n = 0
for img1_lap, img2_lap in zip(laplacian, laplacian2):
    _, rows, _ = img1_lap.shape
    laplacian = np.hstack((img1_lap[:, :int(rows / 2)], img2_lap[:, int(rows / 2):]))
    blend.append(laplacian)

# Реконструируем изображения
blend_reconstructed = blend[0]
for i in range(1, 6):
    size = (blend[i].shape[1], blend[i].shape[0])
    blend_reconstructed = cv2.pyrUp(blend_reconstructed, dstsize=size)
    blend_reconstructed = cv2.add(blend[i], blend_reconstructed)

cv2.imshow("Reconstructed", blend_reconstructed)
cv2.imshow("Just blend", just_blend)
cv2.waitKey(0)
