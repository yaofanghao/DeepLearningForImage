# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 09:15:16 2024

@author: Jerome
"""

import cv2
import numpy as np
import argparse
import os
import shutil

class Set():
    video_path = r"F:\work\sync_work\Fire_detect\pycharm_workplace\pics\12.avi"
    video_name = None
    save_path = ['temp/','temp/单帧火焰/','temp/叠加火焰/']
    thresholds = 160
    backSub = cv2.createBackgroundSubtractorMOG2()
    value = 0.0
    mode = 0


myset = Set()


def my_imread(path):
    cv_img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    return cv_img


def my_imwrite(path,img):
    cv2.imencode('.jpg', img)[1].tofile(path)  # 保存图片


def pre_save():
    try:
        os.makedirs('temp/')
        os.makedirs('temp/单帧火焰')
        os.makedirs('temp/叠加火焰')
    except:
        shutil.rmtree('temp/')
        os.makedirs('temp/')
        os.makedirs('temp/单帧火焰')
        os.makedirs('temp/叠加火焰')

def frame_init():
    parser = argparse.ArgumentParser(description='Fire Detection Program')
    # 添加命令行参数
    parser.add_argument('-p', '--path', type = str, help='input file path', default=myset.video_path)
    parser.add_argument('-t', '--threshold', type = int, help='set the threshold for test', default=myset.thresholds)
    parser.add_argument('-v', '--value', type = float, help='input mode', default=myset.value)
    args = parser.parse_args()

    if args.path is not None:
        myset.video_path = args.path
        myset.video_name = myset.video_path.split('.')[0].split('\\')[-1]

    if args.threshold is not None:
        myset.thresholds = args.threshold

    if args.value is not None:
        myset.value = 1/(args.value ** 2)  # 2024.3.27

    pre_save()
    print("save argument success!")


def back_detect(image, thresholds):
    frame = image
    fgmask = myset.backSub.apply(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 选取前景位置
    nonzero_coords = np.argwhere(fgmask > 0)
    # 提取灰度图中对应位置的像素值
    extracted_gray_image = np.zeros_like(gray)
    for coord in nonzero_coords:
        y, x = coord
        extracted_gray_image[y, x] = gray[y, x]

    _,extracted_gray_image = cv2.threshold(extracted_gray_image, thresholds, 255, cv2.THRESH_BINARY)

    return optimization(extracted_gray_image)



def optimization(image):
    kernel = np.ones((3, 3), np.uint8)

    # 开运算去除小杂点
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)

    # 闭运算连接大块区域
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    return closing


# 保存面积及标定文本所用的程序
def get_txt(index, mode, data):
    if mode == 0:
        txt_name1 = 'temp\单帧像素结果.txt'
        txt_name2 = 'temp\单帧像素结果-仅数字.txt'
        txt_name3 = 'temp\单帧实际结果.txt'
        txt_name4 = 'temp\单帧实际结果-仅数字.txt'
    else:
        txt_name1 = 'temp\叠加像素结果.txt'
        txt_name2 = 'temp\叠加像素结果-仅数字.txt'
        txt_name3 = 'temp\叠加实际结果.txt'
        txt_name4 = 'temp\叠加实际结果-仅数字.txt'
    with open(txt_name1, 'a') as file:
        file.write('第{}帧面积: {}\n'.format(index, data))
        file.close()
    with open(txt_name2, 'a') as file:
        file.write('{}\n'.format(data))
        file.close()
    with open(txt_name3, 'a') as file:
        file.write('第{}帧实际面积: {:.2f}\n'.format(index, data*myset.value))
        file.close()
    with open(txt_name4, 'a') as file:
        file.write('{:.2f}\n'.format(data*myset.value))
        file.close()


def detect_for_all():
    index = 0
    cap = cv2.VideoCapture(myset.video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            if index == 0:
                print("无法打开")
            else:
                res = optimization(image_accumulated)
                name = myset.save_path[0] + myset.video_name
                name += '_thres{}'.format(myset.thresholds)
                name += '_res.png'
                cv2.imwrite(name, res)
                print("Done!")
            break
        else:
            image_backdetect = back_detect(frame, myset.thresholds)
            if index == 0:
                index += 1
                image_accumulated = np.zeros_like(image_backdetect)
                continue
            else:
                image_accumulated = cv2.add(image_accumulated, image_backdetect)
                my_imwrite(myset.save_path[1] + '{}.png'.format(index), image_backdetect)
                my_imwrite(myset.save_path[2] + '{}.png'.format(index), image_accumulated)
                white_area = cv2.countNonZero(image_backdetect)
                get_txt(index, 0, white_area)
                white_area = cv2.countNonZero(image_accumulated)
                get_txt(index, 1, white_area)
                index += 1
    # # 释放资源
    cap.release()
    print("detect success!")


if __name__ == '__main__':
    frame_init()
    detect_for_all()

