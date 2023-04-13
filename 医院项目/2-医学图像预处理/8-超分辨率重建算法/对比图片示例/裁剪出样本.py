# coding:utf-8
import pandas as pd
import os
import cv2

def hisEqulColor(img):
    ## 将RGB图像转换到YCrCb空间中
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # 将YCrCb图像通道分离
    channels = cv2.split(ycrcb)
    # 参考来源： https://docs.opencv.org/4.1.0/d5/daf/tutorial_py_histogram_equalization.html
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe.apply(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img

base_dir = "./source"  #要裁剪的图片的原文件夹位置

output_dir = './source-cut/'  #裁剪后存放的文件夹位置
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

filelist = os.listdir(base_dir)
# filelist.sort(key=lambda x: int(x[:-4]))

for file in filelist:

    path = os.path.join(base_dir, file)
    img = cv2.imread(path, cv2.IMREAD_COLOR)

    filename, _ = os.path.splitext(file)
    cropped = img[1500:2500, 0:1000]

    # cropped = hisEqulColor(cropped)

    save_path = output_dir + str(filename) + '.jpg'  #保存至另一文件夹
    print(save_path)
    cv2.imwrite(save_path, cropped)

