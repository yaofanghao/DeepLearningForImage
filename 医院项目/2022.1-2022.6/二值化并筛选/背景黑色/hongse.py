import cv2
import numpy as np

img = cv2.imread('1.jpg') # 读取照片

#cv2.imshow('img', img) # 显示图像
#cv2.waitKey(0) # 窗口等待的命令，0表示无限等待

rows, cols, channels = img.shape
print(rows, cols, channels)

img2 = cv2.resize(img, None, fx=0.5, fy = 0.5)

rows, cols, channels = img2.shape
print(rows, cols, channels)
cv2.imshow('img', img2)
cv2.waitKey(0)
hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

#cv2.imshow('hsv',hsv)
#cv2.waitKey(0)


lower_blue=np.array([0,10,46])
upper_blue=np.array([180,255,255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)

mask_tmp = cv2.inRange(hsv, lower_blue, upper_blue)

cv2.imshow('mask',mask)
cv2.waitKey(0)
cv2.imwrite('8.jpg',mask)

# 遍历每个像素点，进行颜色的替换
for i in range(rows):
  for j in range(cols):
    if mask[i,j]==255: # 像素点: 255 = 白色
      img2[i,j]=(0,0,255) # 白色 -> 红色
      #img2[i,j]=(0,255,0) # 白色 -> 绿色
      #img2[i,j]=(255,0,0) # 白色 -> 蓝色
      #img2[i,j]=(255,0,255) # 白色 -> 品红色
      #img2[i,j]=(0,255,255) # 白色 -> 黄色
      #img2[i,j]=(255,255,0) # 白色 -> 青色

cv2.imshow('img', img2)
cv2.waitKey(0)
