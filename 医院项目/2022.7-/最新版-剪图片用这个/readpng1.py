# coding:utf-8
import sys
import cv2
import numpy as np
import os
# 设置图片路径，该路径下包含了png格式的照片，名字依次为0.jpg, 1.jpg, 2.jpg,...,14.jpg

DATADIR1 = "C:\\Users\\Lenovo\\Desktop\\cut1\\png"

# 使用os.path模块的join方法生成路径'''
path1 = os.path.join(DATADIR1)
img_list = os.listdir(path1)
ind = 0
#读文件

with open("text1.txt", "r") as f:  # 打开文件
    data = f.read()  # 读取文件

#print(data)

print(type(data))
for i in img_list:
    # 图片文件名称，和代码放在了同一文件夹下
    pathpng = os.path.join(path1, i)
    #print(pathpng)

    # 分离图片名称
    (filepath, tempfilename) = os.path.split(i)
    (filename, extension) = os.path.splitext(tempfilename)
    #print(filename)
    print(type(filename))



