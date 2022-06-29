# coding:utf-8
import pandas as pd
import os
import cv2

base_dir = "./img"  #要裁剪的图片的原文件夹位置

txt_dir = 'new_scores.txt'  #txt文件夹目录

# list = pd.read_csv(txt_dir, sep='\s+',
#                    names=['class1','clas1_score','top','right','left','bottom'])
list = pd.read_csv(txt_dir, sep='\s+',
                   names=['image','score'])
# 图片名先转化为int后分类（sort）
# 按顺序读取图片，这样保证是1,2,3...而不是1,10,11...
filelist = os.listdir(base_dir)
filelist.sort(key=lambda x: int(x.split('.')[0]))

list.index += 1

# print(list)
print(list.iloc[334,0])

# for i in range(0, len(filelist)):
#     name = list.iloc[i, 0]
#     score = list.iloc[i, 1]

sum = 0
threshold = 0.5
for i in range(334,538):
    if list.iloc[i,1] > threshold:
        sum+=1

print("NONNEO分数大于0.5的个数:",sum)
print("所占比例:",round((sum/204)*100,2),str('%'))


