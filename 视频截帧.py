# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:34:26 2020

@author: sheld
"""

import cv2

video_name = 'video';
       
vc = cv2.VideoCapture(video_name + '.avi') #读入视频文件
c=1
 
if vc.isOpened(): #判断是否正常打开
    rval , frame = vc.read()
else:
    rval = False

timeF = 1  #视频帧计数间隔频率
 
while rval:   #循环读取视频帧
    rval, frame = vc.read()
    print(rval,frame)
    if(c%timeF == 0): #每隔timeF帧进行存储操作
        cv2.imwrite('img/'+ str(c) + '.jpg', frame) #存储为图像
    c = c + 1
    cv2.waitKey(1)
    print('success')
vc.release()
