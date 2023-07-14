"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/9 11:50
    @Filename: test.py
    @Software: PyCharm     
"""
import cv2
import numpy as np

# 读取原始图像和模板图像
original_image = cv2.imread('1.jpg')
template_image = cv2.imread('template.jpg')

# 获取模板图像的尺寸
template_height, template_width = template_image.shape[:2]

# 使用TM_CCOEFF_NORMED方法进行模板匹配
result = cv2.matchTemplate(original_image, template_image, cv2.TM_CCOEFF_NORMED)

# 设置匹配阈值，根据具体问题调整
threshold = 0.8

# 使用np.where找到匹配程度超过阈值的位置
locations = np.where(result >= threshold)

# 遍历所有找到的位置并绘制矩形标记
for loc in zip(*locations[::-1]):
    top_left = loc
    bottom_right = (loc[0] + template_width, loc[1] + template_height)
    cv2.rectangle(original_image, top_left, bottom_right, (0, 255, 0), 2)

# 显示匹配结果
resized_image = cv2.resize(original_image, (500,500), interpolation=cv2.INTER_AREA)
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', original_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
