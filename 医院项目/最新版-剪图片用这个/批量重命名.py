# 批量修改图片文件名
import os
import re
import sys

################ 修改内容区域
path = "C:\\Users\\Rainy\\Desktop\\pytroch_aug\\xiuban-aug"
num = 10000
#######################

def renameall(num=num):
    fileList = os.listdir(path)  # 待修改文件夹
    print("修改前：" + str(fileList))  # 输出文件夹中包含的文件
    print("---------------------------------------------------")
    os.chdir(path)  # 将当前工作目录修改为待修改文件夹的位置

    # 名称变量
    # filelist.sort(key=lambda x: int(x[:-4]))
    for fileName in fileList:  # 遍历文件夹中所有文件
        print(fileName)
        pat = ".+\.(jpg|png|gif|json|JPG|xml)"  # 匹配文件名正则表达式
        pattern = re.findall(pat, fileName)  # 进行匹配
        os.rename(fileName, (str(num) + '.' + pattern[0]))  # 文件重新命名

        # ftrainval=open(os.path.join(saveBasePath, 'name.txt'), 'a')
        # ftrainval.write(str(num))
        # ftrainval.write(' ')
        # ftrainval.write(fileName)
        # ftrainval.write("\r")

        print(num)
        num = num + 1


renameall(num=num)
