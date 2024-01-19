import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("8.jpg", flags=1)  # flags=1 读取为彩色图像
imgRef = cv2.imread("template.jpg", flags=1)  # 匹配模板图像 (matching template)

_, _, channel = img.shape
imgOut = np.zeros_like(img)
for i in range(channel):
    print(i)
    histImg, _ = np.histogram(img[:, :, i], 256)  # 计算原始图像直方图
    histRef, _ = np.histogram(imgRef[:, :, i], 256)  # 计算匹配模板直方图
    cdfImg = np.cumsum(histImg)  # 计算原始图像累积分布函数 CDF
    cdfRef = np.cumsum(histRef)  # 计算匹配模板累积分布函数 CDF
    for j in range(256):
        tmp = abs(cdfImg[j] - cdfRef)
        tmp = tmp.tolist()
        index = tmp.index(min(tmp))  # find the smallest number in tmp, get the index of this number
        imgOut[:, :, i][img[:, :, i] == j] = index

fig = plt.figure(figsize=(10, 7))
plt.subplot(231), plt.title("origin"), plt.axis('off')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # 显示原始图像
plt.subplot(232), plt.title("template"), plt.axis('off')
plt.imshow(cv2.cvtColor(imgRef, cv2.COLOR_BGR2RGB))  # 显示匹配模板
plt.subplot(233), plt.title("result"), plt.axis('off')
plt.imshow(cv2.cvtColor(imgOut, cv2.COLOR_BGR2RGB))  # 显示匹配结果
histImg, bins = np.histogram(img.flatten(), 256)  # 计算原始图像直方图
plt.subplot(234, yticks=[]), plt.bar(bins[:-1], histImg)
histRef, bins = np.histogram(imgRef.flatten(), 256)  # 计算匹配模板直方图
plt.subplot(235, yticks=[]), plt.bar(bins[:-1], histRef)
histOut, bins = np.histogram(imgOut.flatten(), 256)  # 计算匹配结果直方图
plt.subplot(236, yticks=[]), plt.bar(bins[:-1], histOut)
plt.show()
