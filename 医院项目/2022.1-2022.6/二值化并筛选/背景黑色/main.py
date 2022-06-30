import cv2
import numpy as np
lenna = cv2.imread("5.jpg")
row, col, channel = lenna.shape
lenna_gray = np.zeros((row, col))
for r in range(row):
    for l in range(col):
        lenna_gray[r, l] = 1 / 3 * lenna[r, l, 0] + 1 / 3 * lenna[r, l, 1] + 1 / 3 * lenna[r, l, 2]
cv2.imwrite('6.jpg',lenna_gray)
cv2.imshow("lenna_gray", lenna_gray.astype("uint8"))
cv2.waitKey()