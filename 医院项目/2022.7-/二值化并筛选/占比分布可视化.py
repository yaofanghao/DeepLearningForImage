# coding:utf-8
import pandas as pd
import matplotlib.pyplot as plt

txt_dir = 'zhanbi.txt'  #txt文件夹目录
list = pd.read_csv(txt_dir, sep='\s+',
                   header=None,
                   names=['image','zhanbi'])
list.index +=1

# print(list.iloc[:,0])  #第0列 image
# print(list.iloc[:,1])  #第1列 zhanbi

plt.figure(figsize=(10,10), dpi=50)
plt.scatter(list.iloc[:,0], list.iloc[:,1])
plt.show()