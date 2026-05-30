'''
Author: yao fanghao
Date: 2023-05-26 14:48:01
LastEditTime: 2023-05-26 15:05:11
LastEditors: yao fanghao
'''
# 2023.5.26
# 读取胃窦胃体文件夹下的xml标签

import numpy
from PIL import Image
import os
import sys
from decimal import Decimal

import xml.etree.ElementTree as ET
def read_xml_name(xml_path):
    # 从xml文件中读取，使用getroot()获取根节点，得到的是一个Element对象
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for object in root.findall('object'):
        class_name = str(object.find('name').text)
        print(class_name)
    tree.write(xml_path)
    return class_name

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("example: python read_xml.py 陈良保")
        name = "陈良保"  
    else:  
        name = sys.argv[1]

    base_dir_path = "img/" + str(name) + "/"
    dir_weidou_path = str(base_dir_path) + "胃窦"
    dir_weiti_path = str(base_dir_path) + "胃体"

    f1 = open(os.path.join(str("img/") + str(name) + '_class_name.txt'), 'a')
    f1.write("【人名：{}】\n".format(str(name)))
    f1.write("【胃窦】\n")

    # ########### ------------ 读取胃窦文件夹中所有xml的标签名
    img_names = os.listdir(dir_weidou_path)
    for xml_name in img_names:
        if xml_name.endswith(".xml"):
            print("读取xml标签中... ", dir_weidou_path, xml_name)
            f1.write((str("/") + str(xml_name)).replace(" ", ""))
            xml_path_ = str(dir_weidou_path) + "/" + str(xml_name)
            class_name = read_xml_name(xml_path=xml_path_)
            f1.write(" {} \n".format(str(class_name)))
    f1.write("\n")

    f1.write("【胃体】\n")
    # ########### ------------ 读取胃体文件夹中所有xml的标签名
    img_names = os.listdir(dir_weiti_path)
    for xml_name in img_names:
        if xml_name.endswith(".xml"):
            print("读取xml标签中... ", dir_weiti_path, xml_name)
            f1.write((str("/") + str(xml_name)).replace(" ", ""))
            xml_path_ = str(dir_weiti_path) + "/" + str(xml_name)
            class_name = read_xml_name(xml_path=xml_path_)
            f1.write(" {} \n".format(str(class_name)))
    f1.write("\n")

    f1.write("\n")
    f1.write("---------------------- \n")
    f1.close()
