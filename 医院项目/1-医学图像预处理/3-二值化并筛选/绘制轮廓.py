import cv2
import numpy as np
img = cv2.imread('1.jpg')    #读取图像z
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #转为灰度值图
# cv2.imshow("gray",gray) #显示灰度图
ret, binary = cv2.threshold(gray,220,255,cv2.THRESH_BINARY) #转为二值图

contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,\
                                       cv2.CHAIN_APPROX_NONE) #寻找轮廓
cv2.imshow("img",img) #显示原图像
img2 = cv2.drawContours(img,contours,-1,(255,255,0),5)  #绘制轮廓,1表示绘制第几个轮廓

cv2.imshow("binary",binary)
img3 = cv2.drawContours(binary,contours,-1,(255,0,0),5)  #绘制轮廓,1表示绘制第几个轮廓

cv2.imshow("contours",img2)   #显示轮廓

cv2.imshow("contours2",img3)   #显示轮廓

cv2.waitKey()
cv2.destroyAllWindows()
#详情见图2效果图
