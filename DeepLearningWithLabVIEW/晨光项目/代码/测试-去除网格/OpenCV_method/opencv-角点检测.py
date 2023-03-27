# https://github.com/opencv/opencv/blob/4.x/samples/python/tutorial_code/TrackingMotion

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(r'test.bmp')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)    #将gray转化为float32的输入图像 blocksize=2，ksize=3
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image　　#将img图像中检测到的角点涂上红色
img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('cornerHarris',img)
cv2.imwrite("cornerHarris.bmp", img)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()