# coding:utf-8
import pandas as pd
import os
import cv2

base_dir = "./img"  #要裁剪的图片的原文件夹位置

# output_dir = './jpg2/'  #裁剪后存放的文件夹位置
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

txt_dir = 'result.txt'  #txt文件夹目录

list = pd.read_csv(txt_dir, sep='\s+',
                   names=['class1','clas1_score','top','right','left','bottom'])

# 图片名先转化为int后分类（sort）
# 按顺序读取图片，这样保证是1,2,3...而不是1,10,11...
filelist = os.listdir(base_dir)
filelist.sort(key=lambda x: int(x.split('.')[0]))

list.index += 1

# print(list)
# print(list.iloc[0,0])

for i in range(0, len(filelist)):

    # path = os.path.join(base_dir, filelist[i])
    # img = cv2.imread(path, cv2.IMREAD_COLOR)

    class1 = list.iloc[i, 0]
    clas1_score = list.iloc[i, 1]
    top = list.iloc[i, 2]
    right = list.iloc[i, 3]
    left = list.iloc[i, 4]
    bottom = list.iloc[i, 5]

    # print(i)
    # print(class1)
    # print(clas1_score)
    # print(top)
    # print(right)
    # print(left)
    # print(bottom)


    # cropped = img[Ymin:Ymax, Xmin:Xmax]
    # cv2.imwrite(path, cropped)
    # save_path = output_dir + str(i+1) + '.jpg'  #保存至另一文件夹
    # cv2.imwrite(save_path, cropped)
    # print('裁剪:%s' % (i+1) )
