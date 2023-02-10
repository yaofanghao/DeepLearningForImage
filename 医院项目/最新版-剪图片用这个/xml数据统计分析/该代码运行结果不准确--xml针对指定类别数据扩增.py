#2023.2.7 针对指定类别的图片进行扩增 扩增后的xml和jpg保存到新文件夹中
# -*- coding: utf-8 -*-

import cv2
import os
import xml.etree.ElementTree as ET
import tqdm

# 水平镜像翻转
def h_MirrorImg(img_path, img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 1)
    cv2.imwrite(img_write_path, mirror_img)

# 垂直翻转
def v_MirrorImg(img_path, img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, 0)
    cv2.imwrite(img_write_path, mirror_img)

# 水平垂直翻转
def a_MirrorImg(img_path, img_write_path):
    img = cv2.imread(img_path)
    mirror_img = cv2.flip(img, -1)
    cv2.imwrite(img_write_path, mirror_img)

def h_MirrorAnno(anno_path, anno_write_path, name):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        x2 = float(bbox.find('xmax').text)
        x1 = w - x1 + 1
        x2 = w - x2 + 1

        assert x1 > 0
        assert x2 > 0

        bbox.find('xmin').text = str(int(x2))
        bbox.find('xmax').text = str(int(x1))

    for node in root.findall('filename'):
        if node != name:
            node.text = name

    tree.write(anno_write_path)  # 保存修改后的XML文件

def v_MirrorAnno(anno_path, anno_write_path, name):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    h = int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        y1 = float(bbox.find('ymin').text)
        y2 = float(bbox.find('ymax').text)
        y1 = h - y1 + 1
        y2 = h - y2 + 1
        assert y1 > 0
        assert y2 > 0
        bbox.find('ymin').text = str(int(y2))
        bbox.find('ymax').text = str(int(y1))

    for node in root.findall('filename'):
        if node != name:
            node.text = name
    tree.write(anno_write_path)  # 保存修改后的XML文件

def a_MirrorAnno(anno_path, anno_write_path, name):
    tree = ET.parse(anno_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    objects = root.findall("object")
    for obj in objects:
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text)
        y1 = float(bbox.find('ymin').text)
        x2 = float(bbox.find('xmax').text)
        y2 = float(bbox.find('ymax').text)
        x1 = w - x1 + 1
        x2 = w - x2 + 1
        y1 = h - y1 + 1
        y2 = h - y2 + 1
        assert x1 > 0
        assert x2 > 0
        assert y1 > 0
        assert y2 > 0
        bbox.find('xmin').text = str(int(x2))
        bbox.find('xmax').text = str(int(x1))
        bbox.find('ymin').text = str(int(y2))
        bbox.find('ymax').text = str(int(y1))

    for node in root.findall('filename'):
        if node != name:
            node.text = name
    tree.write(anno_write_path)  # 保存修改后的XML文件

if __name__ == '__main__':
    img_path = './JPEGImages3342'  # 图片文件夹路径
    xml_path = './Annotations3342'  # xml标注文件夹路径
    img_write_path = './JPEGImages_aug'  # 翻转后的图片保存路径
    xml_write_path = './Annotations_aug'  # 翻转的xml标注保存路径
    if not os.path.exists(img_write_path):
        os.makedirs(img_write_path)
    if not os.path.exists(xml_write_path):
        os.makedirs(xml_write_path)
    flag = 0
    count = 0
    xml_path_list = [os.path.join(xml_path, x) for x in os.listdir(xml_path)]
    for xml in xml_path_list:
        tree = ET.parse(xml_path_list[flag])
        root = tree.getroot()
        for object in root.findall('object'):
            target_name = str(object.find('name').text)
            if target_name == '3' :        # 如果标签为3 则扩增
                filepath, tempfilename = os.path.split(xml_path_list[flag])
                filename, extension = os.path.splitext(tempfilename)
                img_path = os.path.join('./JPEGImages3342', filename+'.jpg')

                h_img_write_path = os.path.join(img_write_path, filename + '_hflip' + '.jpg')
                anno_path = os.path.join(xml_path, filename + '.xml')
                h_anno_write_path = os.path.join(xml_write_path, filename + '_hflip' + '.xml')
                #
                v_img_write_path = os.path.join(img_write_path, filename + '_vflip' + '.jpg')
                v_anno_write_path = os.path.join(xml_write_path, filename + '_vflip' + '.xml')
                #
                a_img_write_path = os.path.join(img_write_path, filename + '_aflip' + '.jpg')
                a_anno_write_path = os.path.join(xml_write_path, filename + '_aflip' + '.xml')
                #
                h_MirrorImg(img_path, h_img_write_path)
                v_MirrorImg(img_path, v_img_write_path)
                a_MirrorImg(img_path, a_img_write_path)
                h_MirrorAnno(anno_path, h_anno_write_path, filename + '_hflip' + '.jpg')
                v_MirrorAnno(anno_path, v_anno_write_path, filename + '_vflip' + '.jpg')
                a_MirrorAnno(anno_path, a_anno_write_path, filename + '_aflip' + '.jpg')
                print("扩增成功:" + img_path)
                flag += 1
                count += 1
            else:
                flag += 1


    print("扩增全部完成！总扩增图片数量为：" + count)





