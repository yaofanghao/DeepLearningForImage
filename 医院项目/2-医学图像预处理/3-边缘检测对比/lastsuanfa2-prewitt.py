# coding:utf-8
import sys
import cv2
import numpy as np
import os

# 设置图片路径
DATADIR = r"E:\MyGithub\cannytest\img1"
output_dir_prewitt = r"E:\MyGithub\cannytest\2-prewitt\\"
output_dir_suanfa2 = r"E:\MyGithub\cannytest\3-suanfa2\\"

if not os.path.exists(output_dir_prewitt):
    os.makedirs(output_dir_prewitt)
if not os.path.exists(output_dir_suanfa2):
    os.makedirs(output_dir_suanfa2)

# 使用os.path模块的join方法生成路径'''
path = os.path.join(DATADIR)
img_list = os.listdir(path)

img_list.sort(key=lambda x:int(x[:-4]))

ind = 0
for i in img_list:
    # 图片文件名称，和代码放在了同一文件夹下
    pathjpg = os.path.join(path, i)
    print(i)

    filename, extension = os.path.splitext(i)

    # opencv读取灰度图像
    img = cv2.imread(pathjpg, cv2.IMREAD_GRAYSCALE)

    # opencv读取彩色图像
    # img = cv2.imread(pathjpg, cv2.IMREAD_COLOR)

    # 灰度图像是二维的，彩色图像是三维的
    h, w = img.shape[:2]

    # Prewitt边缘检测
    # Prewitt算子
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)

    x = cv2.filter2D(img, cv2.CV_16S, kernelx)
    y = cv2.filter2D(img, cv2.CV_16S, kernely)

    # 转 uint8 ,图像融合
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Prewitt = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)

    save_path_prewitt = output_dir_prewitt + str((ind + 1)) + '.jpg'  # 保存至另一文件夹
    cv2.imwrite(save_path_prewitt, Prewitt)
    cv2.imwrite("prewitt.jpg", Prewitt)
    # canny边缘检测
    # original_img = cv2.imread(save_path_sobel, 1)
    # img1 = cv2.GaussianBlur(original_img, (3, 3), 0)
    # canny = cv2.Canny(img1, 50, 150)
    #
    # # 形态学：边缘检测
    # _, Thr_img = cv2.threshold(original_img, 210, 255, cv2.THRESH_BINARY)  # 设定红色通道阈值210（阈值影响梯度运算效果）
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义矩形结构元素
    # gradient = cv2.morphologyEx(Thr_img, cv2.MORPH_GRADIENT, kernel)  # 梯度
    # cv2.imwrite('canny.jpg', canny)
    #
    # ###        边缘检测得出x，y坐标
    # Ymax = 200
    # Ymin = 200
    # Xmax = 200
    # Xmin = 200
    img_path = "prewitt.jpg"
    # # 读取文件
    mat_img = cv2.imread(img_path)
    mat_img2 = cv2.imread(img_path, cv2.CV_8UC1)
    #
    # # 自适应分割
    dst = cv2.adaptiveThreshold(mat_img2, 210, cv2.BORDER_REPLICATE, cv2.THRESH_BINARY_INV, 3, 10)
    # # 提取轮廓
    _, contours, heridency = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # # 标记轮廓
    cv2.drawContours(Prewitt, contours, -1, (255, 0, 255), 3)

    max_area = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area > max_area:
            cnt = contours[i]
            max_area = area

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

    file = open(r'text1.txt', mode='a')  # 将空格写入txt文件中
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

    ##剪原图jpg
    img = cv2.imread(pathjpg)
    #
    cropped = img[Ymin:Ymax, Xmin:Xmax]  # 裁剪坐标为[y0:y1, x0:x1]
    #
    # img_name = str(ind) + '.jpg'
    #
    ind = ind + 1
    # '''生成图片存储的目标路径'''
    save_path = output_dir_suanfa2 + str(ind) + '.jpg'
    cv2.imwrite(save_path, cropped)