import cv2
import numpy as np

# 读取图像
image = cv2.imread('3.jpg', 0)  # 以灰度模式读取图像

# 创建LBP对象
lbp = cv2.face.LBPHFaceRecognizer_create()

# 计算LBP图像
lbp_image = lbp.compute(image)

# 将LBP图像与原始图像相加，得到边缘增强后的图像
enhanced_image = np.add(image, lbp_image)

# 显示原始图像和增强后的图像
cv2.imshow('Original Image', image)
cv2.imshow('Enhanced Image', enhanced_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
