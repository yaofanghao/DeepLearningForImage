import cv2
import numpy as np
import matplotlib.pyplot as plt

def multiScaleRetinex(img, sigma_list):
    retinex = np.zeros_like(img, dtype=np.float64)
    for sigma in sigma_list:
        retinex += np.log10(img) - np.log10(cv2.GaussianBlur(img, (0, 0), sigma))
    retinex = retinex / len(sigma_list)
    return retinex

# 读取图像
img = cv2.imread('6.jpg', 0)

# 定义多尺度sigma值
sigma_list = [15, 80, 250]

# 转换图像数据类型
img_float = np.float64(img)

# 应用多尺度Retinex算法
retinex_img = multiScaleRetinex(img_float, sigma_list)

# 将图像缩放到0-255范围
retinex_img = np.uint8(np.clip((retinex_img - np.min(retinex_img)) / (np.max(retinex_img) - np.min(retinex_img)) * 255, 0, 255))

# 显示原始图像和增强后的图像
plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(retinex_img, cmap='gray')
plt.title('Multi-Scale Retinex Enhanced Image')
plt.axis('off')

plt.show()
