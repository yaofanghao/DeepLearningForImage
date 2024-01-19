"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/11/7 14:45
    @Filename: gabor滤波.py
    @Software: PyCharm     
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

# 读取图像
img = cv2.imread('5.jpg', 0)

# 设置Gabor滤波器的参数
ksize = 31
sigma = 5
theta = 0
lambda_ = 10
gamma = 0.5

# 生成Gabor滤波器
kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambda_, gamma, 0, ktype=cv2.CV_32F)

# 进行滤波
filtered = cv2.filter2D(img, cv2.CV_8UC3, kernel)

# 显示原始图像和滤波后的图像
plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('origin'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(filtered, cmap='gray')
plt.title('Gabor result'), plt.xticks([]), plt.yticks([])
plt.show()