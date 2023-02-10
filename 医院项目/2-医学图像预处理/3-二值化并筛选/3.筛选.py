# coding:utf-8
import pandas as pd
import os
import cv2

output_dir = './erzhihua/'  # 二值化处理后存放的文件夹位置
txt_dir = 'zhanbi.txt'  #txt文件夹目录

thresh = 2 # 自定义设置白色占比的阈值

list = pd.read_csv(txt_dir, sep='\s+',
                   header=None,
                   names=['image','zhanbi'])
list.index +=1

# print(list.iloc[:,0])  #第0列 image
# print(list.iloc[:,1])  #第1列 zhanbi
# print(list)

filelist = os.listdir(output_dir)
filelist.sort(key=lambda x: int(x.split('.')[0]))

list.index +=1

i = 1
flag = 0
for i in range(0, len(filelist)):
    file = open(r'shaixuan.txt', mode='a')  # 将空格写入txt文件中
    file2 = open(r'shaixuan_name.txt', mode='a')

    pathshaixuan = os.path.join(output_dir, filelist[i])
    if list.iloc[i, 1] >= thresh:
        print((str(filelist[i])) + ' ' + str(list.iloc[i,1]))
        file.write(filelist[i])
        file.write(' ')
        file.write(str(list.iloc[i,1]))
        file.write('\n')  # 回车
        file.close()

        head,sep,tail = str(filelist[i]).partition('.')
        file2.write(head)
        file2.write(' ')
        file2.write('\n')  # 回车
        file2.close()

        flag += 1

print('\n')
print('设定白色占比阈值（百分比）：')
print(thresh)
print('要筛选出来超出阈值的图片数：')
print(flag) # 要筛选的图片总数
