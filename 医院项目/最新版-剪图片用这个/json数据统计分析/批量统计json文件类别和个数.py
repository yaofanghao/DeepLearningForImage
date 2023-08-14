"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/19 15:13
    @Filename: 批量统计json文件类别和个数.py
    @Software: PyCharm     
"""
import json
import os
import cv2
import shutil
from tqdm import tqdm

# 待统计图片的标签类别设置
# 旧版-10分类
# class_name = ["duoyuwu", "aokeng", "qipi", "cashang", "gubo",
#               "xiuban", "baiban", "yanghuawu", "huashang","hanjiequexian"]   # 修改点

# 新版-8分类 2023.7.7确定
class_name = ["duoyuwu", "yanghuawu", "gubo", "huashang",
              "qipi", "xiuban", "aokeng", "hanjiequexian"]   # 修改点


# 统计模式设置
# count_mode 为 0
#   一张图中如果有多个相同类别的标注，在统计中对这些每个标注都会加1
# count_mode 为 1
#   对一张图中的多个相同类别的标注只加一次1
count_mode = 1

dir_name = "before/"


# 指定类别的文件夹
save_dir_name = "xiuban/"
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)


# 复制图片到指定文件夹
def copy_image_to_folder(image_path, save_dir_name):
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图片")
        return

    filename = image_path.split("/")[-1]
    destination_path = save_dir_name + filename

    # 复制图片到指定文件夹
    shutil.copyfile(image_path, destination_path)
    print("图片已复制到目标文件夹：", destination_path)


def save_json_to_folder(json_path, save_dir_name):
    filename = json_path.split("/")[-1]
    destination_file = save_dir_name + filename

    # 复制文件到目标文件夹
    shutil.copy(json_path, destination_file)
    print("JSON文件已复制到目标文件夹：", destination_file)


def count_json_label():
    base_path = dir_name
    filelist = os.listdir(base_path)

    dir_count = 0
    d_count, y_count, g_count, h_count, q_count, x_count, a_count, hj_count \
        = 0, 0, 0, 0, 0, 0, 0, 0  # 修改点
    f = open(os.path.join(os.getcwd(), 'json_class_result_mode' + str(count_mode) + '.txt'), 'w')

    if count_mode == 0:
        print("一张图中如果有多个相同类别的标注，在统计中对这些每个标注都会加1")
        f.write("一张图中如果有多个相同类别的标注，在统计中对这些每个标注都会加1")
        for name in tqdm(filelist):
            if (name.endswith(".json")):
                dir_count = dir_count + 1
                filename = os.path.splitext(name)[0]
                filename_suffix = os.path.splitext(name)[1]
                if filename_suffix == ".json":
                    fullname = base_path + filename + filename_suffix
                    dataJson = json.load(open("{}".format(fullname), encoding='UTF-8'))
                    label_name = dataJson["shapes"]
                    d, y, g, h, q, x, a, hj = 0, 0, 0, 0, 0, 0, 0, 0  # 修改点
                    for _ in label_name:
                        d = d + 1 if _["label"] == class_name[0] else d
                        y = y + 1 if _["label"] == class_name[1] else y
                        g = g + 1 if _["label"] == class_name[2] else g
                        h = h + 1 if _["label"] == class_name[3] else h
                        q = q + 1 if _["label"] == class_name[4] else q
                        x = x + 1 if _["label"] == class_name[5] else x
                        a = a + 1 if _["label"] == class_name[6] else a
                        hj = hj + 1 if _["label"] == class_name[7] else hj  # 修改点
                    d_count = d_count + d
                    y_count = y_count + y
                    g_count = g_count + g
                    h_count = h_count + h
                    q_count = q_count + q
                    x_count = x_count + x
                    a_count = a_count + a
                    hj_count = hj_count + hj  # 修改点
                else:
                    pass

    if count_mode == 1:
        print("对一张图中的多个相同类别的标注只加一次1")
        f.write("对一张图中的多个相同类别的标注只加一次1")

        count_flag = 0

        for name in tqdm(filelist):
            if (name.endswith(".json")):
                dir_count = dir_count + 1
                filename = os.path.splitext(name)[0]
                filename_suffix = os.path.splitext(name)[1]
                if filename_suffix == ".json":
                    fullname = base_path + filename + filename_suffix
                    dataJson = json.load(open("{}".format(fullname), encoding='UTF-8'))
                    label_name = dataJson["shapes"]
                    d, y, g, h, q, x, a, hj = 0, 0, 0, 0, 0, 0, 0, 0  # 修改点

                    for _ in label_name:

                        # 筛选出锈斑图，并保存到指定文件夹
                        if _["label"] == class_name[5]:
                            # d = d + 1
                            count_flag = count_flag + 1
                            print("num:{} / image:{} / class:{}".format(count_flag, name, class_name[5]))

                            image_path = dir_name + name.replace('.json','.jpg')
                            json_path = dir_name + name
                            print(image_path)
                            print(json_path)
                            copy_image_to_folder(image_path, save_dir_name)
                            save_json_to_folder(json_path, save_dir_name)

                        y = y + 1 if _["label"] == class_name[1] else y
                        g = g + 1 if _["label"] == class_name[2] else g
                        h = h + 1 if _["label"] == class_name[3] else h
                        q = q + 1 if _["label"] == class_name[4] else q
                        x = x + 1 if _["label"] == class_name[5] else x
                        a = a + 1 if _["label"] == class_name[6] else a
                        hj = hj + 1 if _["label"] == class_name[7] else hj  # 修改点

                    # 对同个图片中的同个标注，只统计一次
                    d = 1 if d > 1 else d
                    y = 1 if y > 1 else y
                    g = 1 if g > 1 else g
                    h = 1 if h > 1 else h
                    q = 1 if q > 1 else q
                    x = 1 if x > 1 else x
                    a = 1 if a > 1 else a
                    hj = 1 if hj > 1 else hj  # 修改点

                    d_count = d_count + d
                    y_count = y_count + y
                    g_count = g_count + g
                    h_count = h_count + h
                    q_count = q_count + q
                    x_count = x_count + x
                    a_count = a_count + a
                    hj_count = hj_count + hj   # 修改点
                else:
                    pass
    else:
        raise AssertionError("请输入正确的统计模式 0 / 1")

    print("json文件总个数:" + str(dir_count))
    print("具体标签统计结果如下：")
    print("     " + str(class_name[0]) + ": " + str(d_count))
    print("     " + str(class_name[1]) + ": " + str(y_count))
    print("     " + str(class_name[2]) + ": " + str(g_count))
    print("     " + str(class_name[3]) + ": " + str(h_count))
    print("     " + str(class_name[4]) + ": " + str(q_count))
    print("     " + str(class_name[5]) + ": " + str(x_count))
    print("     " + str(class_name[6]) + ": " + str(a_count))
    print("     " + str(class_name[7]) + ": " + str(hj_count))  # 修改点

    f.write("\n")
    f.write("json文件总个数:" + str(dir_count))
    f.write("\n")
    f.write("具体标签统计结果如下：")
    f.write("\n")
    f.write("     " + str(class_name[0]) + ": " + str(d_count))
    f.write("\n")
    f.write("     " + str(class_name[1]) + ": " + str(y_count))
    f.write("\n")
    f.write("     " + str(class_name[2]) + ": " + str(g_count))
    f.write("\n")
    f.write("     " + str(class_name[3]) + ": " + str(h_count))
    f.write("\n")
    f.write("     " + str(class_name[4]) + ": " + str(q_count))
    f.write("\n")
    f.write("     " + str(class_name[5]) + ": " + str(x_count))
    f.write("\n")
    f.write("     " + str(class_name[6]) + ": " + str(a_count))
    f.write("\n")
    f.write("     " + str(class_name[7]) + ": " + str(hj_count))  # 修改点

# 将标签duoyvwu替换为duoyuwu
def replace_label_name():
    json_dir = dir_name  # 写入json文件的文件夹路径
    json_files = os.listdir(json_dir)

    # 写自己的旧标签名和新标签名
    old_name = "duoyvwu"
    new_name = "duoyuwu"

    for json_file in json_files:
        json_file_ext = os.path.splitext(json_file)

        if json_file_ext[1] == '.json':
            jsonfile = json_dir + json_file

            with open(jsonfile, 'r', encoding='utf-8') as jf:
                info = json.load(jf)

                for i, label in enumerate(info['shapes']):
                    if info['shapes'][i]['label'] == old_name:
                        info['shapes'][i]['label'] = new_name
                        # 找到位置进行修改
                        print('{} change name over!'.format(json_file))
                    # else:
                        # print('{} do not change name!'.format(json_file))

                # 使用新字典替换修改后的字典
                json_dict = info

            # 将替换后的内容写入原文件
            with open(jsonfile, 'w') as new_jf:
                json.dump(json_dict, new_jf)



if __name__ == '__main__':

    replace_label_name()

    count_json_label()