# -*- coding: utf-8 -*-
import os
def rename():
    count=1 #初始文件编号为1
    path= 'images'  #需要重命名的文件目录，注意目录的写法
    filelist=os.listdir(path) #返回指定的文件夹包含的文件或文件夹的名字的列表。这个列表以字母顺序。
    for files in filelist:  #循环列出文件
        Olddir=os.path.join(path,files)  #将多个路径组合后返回
        if os.path.isdir(Olddir): #判断路径是否为目录，isfile判断是否为文件
            continue #是的话继续
        filename=os.path.splitext(files)[0]  #文件名
        filetype=os.path.splitext(files)[1]  #文件后缀
        Newdir=os.path.join(path,'img_'+str(count)+filetype)
        os.rename(Olddir,Newdir)  #重命名文件或目录
        count+=1   #文件编号加1
rename()
