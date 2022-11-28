
from PIL import Image
from PIL import ImageEnhance
import numpy as np

import json
import os


def FZ(AnnotFilePath, SaveDataDir):
    img = np.asarray(Image.open(AnnotFilePath))  # 读取图像
    # img1 = np.flip(img, 0)  # 上下翻转
    img1 = np.fliplr(img)  # 左右翻转

    # enh_con = ImageEnhance.Contrast(img)
    # contrast = 1.4
    # img1 = enh_con.enhance(contrast)

    #保存
    _, AnnotFileName = os.path.split(AnnotFilePath)
    NewPath = os.path.join(SaveDataDir, AnnotFileName)
    Image.fromarray(img1).save(NewPath)
    print(1)


file='E:\MyGithub\MyLabVIEW\晨光项目\代码\测试-去除网格\数据集制作\png2'
alist = os.listdir(file)
for i in range(0, len(alist)):
    path = os.path.join(file, alist[i])
    AnnotFilePath = path
    SaveDataDir = 'E:\MyGithub\MyLabVIEW\晨光项目\代码\测试-去除网格\数据集制作\png3'
    FZ(AnnotFilePath, SaveDataDir)  # 使用for循环批量转化

