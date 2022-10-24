# coding:utf-8
import sys
import cv2
import numpy as np
import os

# 设置图片路径
DATADIR = r"C:\Users\admin\Desktop\dataset\jpg1"

# 使用os.path模块的join方法生成路径'''
path = os.path.join(DATADIR)
#path1 = os.path.join(DATADIR1)
img_list = os.listdir(path)

#按顺序
img_list.sort(key=lambda x:int(x[:-4]))


ind = 0
for i in img_list:
    # 图片文件名称，和代码放在了同一文件夹下
    pathjpg = os.path.join(path, i)
    print(i)

    filename, extension = os.path.splitext(i)
    #print(extension)
    #print("需要分离的完整文件名：" + path)
    #print("文件名称：" + filename + "\t\t\t\t后缀：" + extension)

    # opencv读取灰度图像
    img = cv2.imread(pathjpg, cv2.IMREAD_GRAYSCALE)

    # opencv读取彩色图像
    img = cv2.imread(pathjpg, cv2.IMREAD_COLOR)

    # 灰度图像是二维的，彩色图像是三维的
    h, w = img.shape[:2]

    # 索贝尔水平检测
    sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)

    # 原图显示
    # cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    # cv2.imshow('Original', img)
    # cv2.waitKey()
    # 索贝尔水平
    # cv2.namedWindow('Sobel horizontal', cv2.WINDOW_NORMAL)
    #cv2.imshow('Sobel horizontal', sobel_horizontal)
    cv2.imwrite('Sobel horizontal.jpg', sobel_horizontal)
    # cv2.waitKey()
    original_img = cv2.imread("Sobel horizontal.jpg", 1)

    # canny(): 边缘检测
    img1 = cv2.GaussianBlur(original_img, (3, 3), 0)
    canny = cv2.Canny(img1, 50, 150)

    # 形态学：边缘检测
    _, Thr_img = cv2.threshold(original_img, 210, 255, cv2.THRESH_BINARY)  # 设定红色通道阈值210（阈值影响梯度运算效果）
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义矩形结构元素
    gradient = cv2.morphologyEx(Thr_img, cv2.MORPH_GRADIENT, kernel)  # 梯度
    # cv2.namedWindow('original_img',cv2.WINDOW_NORMAL)
    # cv2.namedWindow('gradient',cv2.WINDOW_NORMAL)
    #cv2.namedWindow('Canny',cv2.WINDOW_NORMAL)
    # cv2.imshow("original_img", original_img)
    # cv2.imshow("gradient", gradient)
    #cv2.imshow('Canny', canny)

    cv2.imwrite('canny.jpg', canny)

    # cv2.waitKey(0)

    # cv2.destroyAllWindows()
    # cv2.waitKey()

    # coding=gbk

    # C:\\Users\\Lenovo\\Desktop\\cut\\jpg\\image74.jpg"

    ###        边缘检测得出x，y坐标
    Ymax = 200
    Ymin = 200
    Xmax = 200
    Xmin = 200
    img_path = "canny.jpg"
    # 读取文件
    mat_img = cv2.imread(img_path)
    mat_img2 = cv2.imread(img_path, cv2.CV_8UC1)

    # 自适应分割
    dst = cv2.adaptiveThreshold(mat_img2, 210, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 3, 10)
    # 提取轮廓
    contours, heridency = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 标记轮廓
    cv2.drawContours(mat_img, contours, -1, (255, 0, 255), 3)
    #print(type(contours))
    # 计算轮廓面积
    # 计算轮廓面积
    # area = 0
    # for i in contours:
    #    area += cv2.contourArea(i)
    # print(area)

    max_area = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > max_area:
            cnt = contours[i]
            max_area = area
        # print(max_area)
        # print(i)
    #print(max_area)

    # 计算轮廓面积
    Area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if (Area < area):
            Area = area
    #print(Area)
    Hmax = 0
    Wmax = 0
    if len(contours) > 0:
        # cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和高
        boxes = [cv2.boundingRect(c) for c in contours]
        for box in boxes:
            x, y, w, h = box

            if (Hmax < h):
                Hmax = h
                Ymin = y
                Ymax = y + Hmax
            if (Wmax < w):
                Wmax = w
                Xmin = x
                Xmax = x + Wmax
            # 绘制矩形框对轮廓进行定位
            cv2.rectangle(mat_img, (x, y), (x + w, y + h), (153, 153, 0), 2)

    #print(Hmax)
    #print(Wmax)

    #print(Ymin)
    #print(Ymax)

    #print(Xmin)
    #print(Xmax)
    file = open(r'text1.txt', mode='a')  # 将空格写入txt文件中
    #file.write(' ')
    #file.write(filename)
    file.write(' ')
    file.write(str(Ymin))
    file.write(' ')
    file.write(str(Ymax))
    file.write(' ')
    file.write(str(Xmin))
    file.write(' ')
    file.write(str(Xmax))
    file.write(' ')
    file.write('\n')  # 将回车写入txt文件中
    file.close()

    # 图像show
    #cv2.namedWindow('juxing',cv2.WINDOW_NORMAL)
    #cv2.imshow("juxing",mat_img)
    #cv2.imwrite('juxing.jpg', mat_img)
    #cv2.waitKey(0)

    ##剪原图jpg
    img = cv2.imread(pathjpg)

    #cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    #cv2.imshow("img", img)
    # cv2.namedWindow('cut1',cv2.WINDOW_NORMAL)
    cropped = img[Ymin:Ymax, Xmin:Xmax]  # 裁剪坐标为[y0:y1, x0:x1]
    #cv2.namedWindow('cut1',cv2.WINDOW_NORMAL)
    #cv2.imshow("cut1",cropped)

    img_name = str(ind) + '.jpg'

    ind = ind + 1
    # '''生成图片存储的目标路径'''
    save_path = "C:\\Users\\admin\\Desktop\\dataset\\jpg2\\" + str(ind) + '.jpg'


    # '''调用cv.2的imwrite函数保存图片'''
    cv2.imwrite(save_path, cropped)
    # cv2.imwrite(save_path1, cropped1)
    #cv2.waitKey(0)
