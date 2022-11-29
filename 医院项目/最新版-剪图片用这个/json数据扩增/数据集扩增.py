from PIL import Image
from PIL import ImageEnhance
import numpy as np
import json
import os

#######################
# 修改内容区域：
file='C:\\Users\\Lenovo\\Desktop\\12月27号\\make-dataset\\jpg'  # 原图文件夹  
SaveDataDir = 'C:\\Users\\Lenovo\\Desktop\\12月27号\\make-dataset\\翻转jpg'  #扩增后图片的文件夹
#######################

if __name__ == '__main__':
    alist = os.listdir(file)
    for i in range(0, len(alist)):
        path = os.path.join(file, alist[i])
        AnnotFilePath = path

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
        print(i)

