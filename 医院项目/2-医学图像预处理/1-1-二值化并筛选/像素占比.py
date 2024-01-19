import cv2
import  numpy as np

img=cv2.imread('1.jpg',cv2.IMREAD_GRAYSCALE) #灰度图像
x,y= img.shape
print(x)

print(img.shape)

# #遍历灰度图，阈值大于的全变白
for i in range(x):
    for j in range(y):
        if img[i,j]>0:
            img[i,j]=255
        else:
            img[i,j]=0
black = 0
white = 0
#遍历二值图，为0则black+1，否则white+1
for i in range(x):
    for j in range(y):
        if img[i,j]==0:
            black+=1
        else:
            white+=1
print("白色个数:",white)
print("黑色个数:",black)
rate1 = white/(x*y)
rate2 = black/(x*y)
print(white+black)

rate1 = white/(white+black)
rate2 = black/(white+black)

print("白色占比:", round(rate1*100,2),'%')
print("黑色占比:", round(rate2*100,2),'%')

