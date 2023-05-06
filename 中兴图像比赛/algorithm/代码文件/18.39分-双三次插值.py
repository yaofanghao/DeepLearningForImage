# coding=utf-8
import os
from PIL import Image
import numpy as np
import math
from tqdm import tqdm

# 产生16个像素点不同的权重
def BiBubic(x):
    x=abs(x)
    if x<=1:
        return 1-2*(x**2)+(x**3)
    elif x<2:
        return 4-8*x+5*(x**2)-(x**3)
    else:
        return 0

# 双三次插值算法
def BiCubic_interpolation(img,dstH,dstW):
    scrH,scrW,_=img.shape
    #img=np.pad(img,((1,3),(1,3),(0,0)),'constant')
    retimg=np.zeros((dstH,dstW,3),dtype=np.uint8)
    for i in tqdm(range(dstH)):
        for j in range(dstW):
            scrx=i*(scrH/dstH)
            scry=j*(scrW/dstW)
            x=math.floor(scrx)
            y=math.floor(scry)
            u=scrx-x
            v=scry-y
            tmp=0
            for ii in range(-1,2):
                for jj in range(-1,2):
                    if x+ii<0 or y+jj<0 or x+ii>=scrH or y+jj>=scrW:
                        continue
                    tmp+=img[x+ii,y+jj]*BiBubic(ii-u)*BiBubic(jj-v)
            retimg[i,j]=np.clip(tmp,0,255)
            # print("calculate...."+str(i)+"_"+str(j))
    return retimg

if __name__ == '__main__':

    #目标文件夹路径
    determination = './output'
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
            else:
                dst_shape0 = 720
                dst_shape1 = 1280
            # 双三次插值 效果不太好
            deter_dir = determination + '/' + str(folder)
            if not os.path.exists(deter_dir):
                os.makedirs(deter_dir)
            deter = deter_dir + '/' + str(file)
            print("image source is:", source)
            print("image save to:", deter)
            image2 = BiCubic_interpolation(image, dst_shape0, dst_shape1)
            image2 = Image.fromarray(image2.astype('uint8')).convert('RGB')
            image2.save(deter)
            flag = flag+1
            print("success, number is ", flag)
