# coding:utf-8
import os
import pandas as pd

#######################
# 修改以下三项：
path = './png4/'  # 要改名的文件夹
output_dir = './png4/'  #重命名后存放的文件夹
txt_dir = 'name.txt'   # txt文件夹
#######################

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

filelist = os.listdir(path)
filelist.sort(key=lambda x: int(x.split('.')[0]))

list = pd.read_csv(txt_dir, sep='\s+',
                   encoding='utf-8',
                   index_col=0,
                   names=['name','name_num'])
# list.index +=1

# print(list)
# print(list['name']+list['name_num'])

print(list.iloc[0,0]+list.iloc[0,1])

for item in filelist:
    if (item.endswith('.png')):
        for i in range(0, len(filelist)):
            src = os.path.join(path, filelist[i])   # 原名位置
            name = (list.iloc[i, 0]+list.iloc[i,1])
            dst = os.path.join(output_dir, name)  #改名后位置
            os.rename(src, dst)  # 重命名
            print ('convert %s to %s ...' % (i+1, name))
            i = i + 1
