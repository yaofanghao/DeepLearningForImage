# coding:utf-8
import os
from PIL import Image

# 生成图片尺寸的txt
def generate_jpg_size(base_dir):
    filelist = os.listdir(base_dir)
    filelist.sort(key=lambda x: int(x.split('.')[0]))
    i = 1
    for i in range(0, len(filelist)):
        path = os.path.join(base_dir, filelist[i])
        img = Image.open(path)
        # print(img.width, img.height)
        print("read jpg " + str(i+1))
        ftrainval=open(os.path.join('./jpg_size.txt'), 'a') # 存储为txt
        ftrainval.write(str(i+1))
        ftrainval.write(' ')
        ftrainval.write(str(img.width))
        ftrainval.write(' ')
        ftrainval.write(str(img.height))
        ftrainval.write("\r")

def generate_png_size(base_dir1):
    filelist = os.listdir(base_dir1)
    filelist.sort(key=lambda x: int(x.split('.')[0]))
    i = 1
    for i in range(0, len(filelist)):
        path = os.path.join(base_dir1, filelist[i])
        img = Image.open(path)
        # print(img.width, img.height)
        print("read png " + str(i+1))
        ftrainval=open(os.path.join('./png_size.txt'), 'a')
        ftrainval.write(str(i+1))
        ftrainval.write(' ')
        ftrainval.write(str(img.width))
        ftrainval.write(' ')
        ftrainval.write(str(img.height))
        ftrainval.write("\r")

# 比较两个txt的差异
import difflib
def compare_txt(file_1,file_2):
    # 打开文件
    # 按行分割文件,返回的是列表
    a = file_1.read().splitlines()
    b = file_2.read().splitlines()
    # print(set(a)-set(b))
    # difflib库显示逐行差异，a文件的第一行跟b文件的第一行去比较
    dif = difflib.Differ().compare(a, b)
    for i in dif:
        print(i)
    # 关闭文件
    file_1.close()
    file_2.close()

if __name__ == '__main__':
    base_dir = "./jpg3"  # jpg目录
    base_dir1 = "./png3" # png目录

    generate_jpg_size(base_dir)
    generate_png_size(base_dir1)

    file_1 = open(r'./jpg_size.txt', 'r')
    file_2 = open(r'./png_size.txt', 'r')

    compare_txt(file_1,file_2)