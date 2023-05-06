# coding=utf-8
import os
from PIL import Image
import numpy as np
import cv2

if __name__ == '__main__':

    #目标文件夹路径
    determination = './data'
    if not os.path.exists(determination):
        os.makedirs(determination)

    #原文件夹总的路径
    path = './data'
    folders = os.listdir(path)

    flag = 0
    for folder in folders:
        dirs = path + '/' + str(folder)
        dirs_dir = os.listdir(dirs)
        for file in dirs_dir:
            source = dirs + '/' + str(file)

            # source 原图所在路径
            # deter 处理后图片保存路径
            image = np.array(Image.open(source))
            if (image.shape[0] >= image.shape[1]):
                dst_shape0 = 1280
                dst_shape1 = 720
                image2 = cv2.resize(image, (dst_shape1, dst_shape0), interpolation=cv2.INTER_AREA)
            else:
                dst_shape0 = 720
                dst_shape1 = 1280
                image2 = cv2.resize(image, (dst_shape1, dst_shape0), interpolation=cv2.INTER_AREA)
            deter_dir = determination + '/' + str(folder)
            if not os.path.exists(deter_dir):
                os.makedirs(deter_dir)
            deter = deter_dir + '/' + str(file)
            print("image source is:", source)
            print("image save to:", deter)
            image2 = Image.fromarray(image2.astype('uint8')).convert('RGB')
            image2.save(deter)
            flag = flag+1
            print("success, number is ", flag)
