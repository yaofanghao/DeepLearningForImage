# coding:utf-8
import pandas as pd
import os
import cv2

base_dir = "./png2"  #要裁剪的图片的原文件夹位置

output_dir = './png3/'  #裁剪后存放的文件夹位置
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

txt_dir = 'text2.txt'  #txt文件夹目录

list = pd.read_csv(txt_dir, sep='\s+',
                   names=['Ymin','Ymax','Xmin','Xmax'])

# 图片名先转化为int后分类（sort）
# 按顺序读取图片，这样保证是1,2,3...而不是1,10,11...
filelist = os.listdir(base_dir)
filelist.sort(key=lambda x: int(x.split('.')[0]))

list.index +=1

# print(list.iloc[:,0])  #第0列 Ymin
# print(list.iloc[:,1])  #第1列 Ymax
# print(list.iloc[:,2])  #第2列 Xmin
# print(list.iloc[:,3])  #第3列 Xmax
# print(list)

i = 1
for i in range(0, len(filelist)):

    path = os.path.join(base_dir, filelist[i])
    img = cv2.imread(path, cv2.IMREAD_COLOR)

    Ymin = list.iloc[i, 0]
    Ymax = list.iloc[i, 1]
    Xmin = list.iloc[i, 2]
    Xmax = list.iloc[i, 3]

    cropped = img[Ymin:Ymax, Xmin:Xmax]

    # cv2.imwrite(path, cropped)

    save_path = output_dir + str(i+1) + '.png'  #保存至另一文件夹
    cv2.imwrite(save_path, cropped)

    print('裁剪:%s' % (i+1) )
