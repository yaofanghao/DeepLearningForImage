"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/25 16:27
    @Filename: read_txt.py
    @Software: PyCharm     
"""
# f = open("class_name.txt", "r")
#
# lines = f.readlines()
# for i in range(len(lines)):
#     print(lines[i], end='')

classes_txt = "class_name.txt"
classes_gbk_txt = "class_name_gbk.txt"

def read_txt_lines(classes_txt=None, classes_gbk_txt=None):
    name_classes = []
    name_classes_gbk = []
    f = open(classes_txt, "r")
    f_gbk = open(classes_gbk_txt, "r", encoding='utf-8')
    lines = f.read().splitlines()
    lines_gbk = f_gbk.read().splitlines()
    for i in range(len(lines)):
        name_classes.append(lines[i])
        name_classes_gbk.append(lines_gbk[i])
    return name_classes, name_classes_gbk

name_classes, name_classes_gbk = read_txt_lines(classes_txt, classes_gbk_txt)
print("success")
