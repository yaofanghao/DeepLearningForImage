# https://blog.csdn.net/Eastmount/article/details/126799744

# -*- coding: utf-8 -*-
# By：Eastmount
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('1.jpg')

# 彩色图像均衡化 需要分解通道 对每一个通道均衡化
(b, g, r) = cv2.split(img)
bH = cv2.equalizeHist(b)
gH = cv2.equalizeHist(g)
rH = cv2.equalizeHist(r)

# 合并每一个通道
result = cv2.merge((bH, gH, rH))
cv2.imshow("Input", img)
cv2.imshow("Result", result)
cv2.imwrite("1_out.jpg",result)

cv2.waitKey(0)
cv2.destroyAllWindows()

plt.figure("Hist")
#蓝色分量
plt.hist(bH.ravel(), bins=256, normed=1, facecolor='b', edgecolor='b', hold=1)
#绿色分量
plt.hist(gH.ravel(), bins=256, normed=1, facecolor='g', edgecolor='g', hold=1)
#红色分量
plt.hist(rH.ravel(), bins=256, normed=1, facecolor='r', edgecolor='r', hold=1)
plt.xlabel("x")
plt.ylabel("y")
plt.show()