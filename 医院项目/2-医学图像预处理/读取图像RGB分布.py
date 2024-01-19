"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/11/7 16:52
    @Filename: 读取图像RGB分布.py
    @Software: PyCharm     
"""

import cv2
import matplotlib.pyplot as plt

# 读取彩色图像
img = cv2.imread('5.jpg')

# 将图像从BGR颜色空间转换为RGB颜色空间
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 获取图像的高度、宽度和通道数
h, w, _ = img_rgb.shape

# 将图像的RGB通道分离
r, g, b = cv2.split(img_rgb)

# 计算每个通道的像素分布
r_hist = cv2.calcHist([r], [0], None, [256], [0, 256]) / (h * w)
g_hist = cv2.calcHist([g], [0], None, [256], [0, 256]) / (h * w)
b_hist = cv2.calcHist([b], [0], None, [256], [0, 256]) / (h * w)

# 绘制RGB分布曲线
plt.plot(r_hist, color='red', label='Red Channel')
plt.plot(g_hist, color='green', label='Green Channel')
plt.plot(b_hist, color='blue', label='Blue Channel')
plt.title('RGB Distribution Curve')
plt.xlabel('Pixel Value')
plt.ylabel('Normalized Frequency')
plt.legend()
plt.show()
