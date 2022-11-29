# coding:utf-8
import sys
import cv2
import numpy as np
import os

if __name__ == '__main__':
    #######################
    # 修改内容区域：
    DATADIR1 = "C:\\Users\\Lenovo\\Desktop\\cut1\\png"
    ####################### 

    if not os.path.exists(DATADIR1):
        os.makedirs(DATADIR1)
    path1 = os.path.join(DATADIR1)
    img_list = os.listdir(path1)
    ind = 0

    with open("text1.txt", "r") as f:  
        data = f.read() 

    print(type(data))
    for i in img_list:
        # 图片文件名称，和代码放在了同一文件夹下
        pathpng = os.path.join(path1, i)
        #print(pathpng)

        filepath, tempfilename = os.path.split(i)
        filename, extension = os.path.splitext(tempfilename)
        #print(filename)
        print(type(filename))



