# https://pytorch.org/vision/stable/transforms.html
# http://news.sohu.com/a/595439338_121124378

import os
import numpy as np
import cv2 as cv
import PIL.Image as Image
import torch
from torchvision import transforms
import matplotlib.pyplot as plt


################ 修改内容区域
DATADIR = "xiuban"  # 原图片路径
save_dir = "xiuban-aug\\"  # 处理后图片路径
#######################

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
path = os.path.join(DATADIR)
img_list = os.listdir(path)


def transform_(img):

    # 图像增强设置区域
    brightness_transform = transforms.ColorJitter(brightness=(1.5,1.6))
    contrast_transform = transforms.ColorJitter(contrast=(1.2,1.3))
    saturation_transform = transforms.ColorJitter(saturation=(1.1,1.2))
    hue_transform = transforms.ColorJitter(hue=(0.01,0.02))

    transform = transforms.Compose([brightness_transform,
                                    contrast_transform,
                                    saturation_transform,
                                    hue_transform])
    res = transform(img)

    return res

# img_list.sort(key=lambda x: int(x[:-4]))
for i in img_list:
    pathjpg = os.path.join(path, i)
    print(i)
    filename, extension = os.path.splitext(i)
    img = Image.open(pathjpg)

    # 图像处理模块
    res = transform_(img=img)
    # res, factor = data_augment_demo(res, 0.5)
    # res = convert_white(res)

    # 保存图片，解决了中文路径报错的问题
    save_path = save_dir + str(filename) + '.jpg'
    res.save(save_path)


