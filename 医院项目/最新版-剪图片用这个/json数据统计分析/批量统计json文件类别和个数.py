"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/19 15:13
    @Filename: 批量统计json文件类别和个数.py
    @Software: PyCharm     
"""
import json
import os
from tqdm import tqdm

# 待统计图片的标签类别设置
class_name = ["duoyuwu", "aokeng", "qipi", "cashang", "gubo",
              "xiuban", "baiban", "yanghuawu", "huashang","hanjiequexian"]   # 修改点

# 统计模式设置
# count_mode 为 0
#   一张图中如果有多个相同类别的标注，在统计中对这些每个标注都会加1
# count_mode 为 1
#   对一张图中的多个相同类别的标注只加一次1
count_mode = 1

dir_name = "6.25-before/"

def count_json_label():
    base_path = dir_name
    filelist = os.listdir(base_path)

    dir_count = 0
    d_count, a_count, q_count, c_count, g_count, x_count, b_count, y_count, h_count, hj_count \
        = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0   # 修改点
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
                    d, a, q, c, g, x, b, y, h, hj = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 修改点
                    for _ in label_name:
                        d = d + 1 if _["label"] == class_name[0] else d
                        a = a + 1 if _["label"] == class_name[1] else a
                        q = q + 1 if _["label"] == class_name[2] else q
                        c = c + 1 if _["label"] == class_name[3] else c
                        g = g + 1 if _["label"] == class_name[4] else g
                        x = x + 1 if _["label"] == class_name[5] else x
                        b = b + 1 if _["label"] == class_name[6] else b
                        y = y + 1 if _["label"] == class_name[7] else y
                        h = h + 1 if _["label"] == class_name[8] else h
                        hj = hj + 1 if _["label"] == class_name[9] else hj  # 修改点
                    d_count = d_count + d
                    a_count = a_count + a
                    q_count = q_count + q
                    c_count = c_count + c
                    g_count = g_count + g
                    x_count = x_count + x
                    b_count = b_count + b
                    y_count = y_count + y
                    h_count = h_count + h
                    hj_count = hj_count + hj   # 修改点
                else:
                    pass

    if count_mode == 1:
        print("对一张图中的多个相同类别的标注只加一次1")
        f.write("对一张图中的多个相同类别的标注只加一次1")
        for name in tqdm(filelist):
            if (name.endswith(".json")):
                dir_count = dir_count + 1
                filename = os.path.splitext(name)[0]
                filename_suffix = os.path.splitext(name)[1]
                if filename_suffix == ".json":
                    fullname = base_path + filename + filename_suffix
                    dataJson = json.load(open("{}".format(fullname), encoding='UTF-8'))
                    label_name = dataJson["shapes"]
                    d, a, q, c, g, x, b, y, h, hj = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  # 修改点


                    for _ in label_name:
                        d = d + 1 if _["label"] == class_name[0] else d
                        a = a + 1 if _["label"] == class_name[1] else a
                        q = q + 1 if _["label"] == class_name[2] else q
                        c = c + 1 if _["label"] == class_name[3] else c
                        g = g + 1 if _["label"] == class_name[4] else g
                        x = x + 1 if _["label"] == class_name[5] else x
                        b = b + 1 if _["label"] == class_name[6] else b
                        y = y + 1 if _["label"] == class_name[7] else y
                        h = h + 1 if _["label"] == class_name[8] else h
                        hj = hj + 1 if _["label"] == class_name[9] else hj  # 修改点

                    # 对同个图片中的同个标注，只统计一次
                    d = 1 if d > 1 else d
                    a = 1 if a > 1 else a
                    q = 1 if q > 1 else q
                    c = 1 if c > 1 else c
                    g = 1 if g > 1 else g
                    x = 1 if x > 1 else x
                    b = 1 if b > 1 else b
                    y = 1 if y > 1 else y
                    h = 1 if h > 1 else h
                    hj = 1 if hj > 1 else hj  # 修改点

                    d_count = d_count + d
                    a_count = a_count + a
                    q_count = q_count + q
                    c_count = c_count + c
                    g_count = g_count + g
                    x_count = x_count + x
                    b_count = b_count + b
                    y_count = y_count + y
                    h_count = h_count + h
                    hj_count = hj_count + hj   # 修改点
                else:
                    pass
    else:
        raise AssertionError("请输入正确的统计模式 0 / 1")

    print("json文件总个数:" + str(dir_count))
    print("具体标签统计结果如下：")
    print("     " + str(class_name[0]) + ": " + str(d_count))
    print("     " + str(class_name[1]) + ": " + str(a_count))
    print("     " + str(class_name[2]) + ": " + str(q_count))
    print("     " + str(class_name[3]) + ": " + str(c_count))
    print("     " + str(class_name[4]) + ": " + str(g_count))
    print("     " + str(class_name[5]) + ": " + str(x_count))
    print("     " + str(class_name[6]) + ": " + str(b_count))
    print("     " + str(class_name[7]) + ": " + str(y_count))
    print("     " + str(class_name[8]) + ": " + str(h_count))
    print("     " + str(class_name[9]) + ": " + str(hj_count)) # 修改点

    f.write("\n")
    f.write("json文件总个数:" + str(dir_count))
    f.write("\n")
    f.write("具体标签统计结果如下：")
    f.write("\n")
    f.write("     " + str(class_name[0]) + ": " + str(d_count))
    f.write("\n")
    f.write("     " + str(class_name[1]) + ": " + str(a_count))
    f.write("\n")
    f.write("     " + str(class_name[2]) + ": " + str(q_count))
    f.write("\n")
    f.write("     " + str(class_name[3]) + ": " + str(c_count))
    f.write("\n")
    f.write("     " + str(class_name[4]) + ": " + str(g_count))
    f.write("\n")
    f.write("     " + str(class_name[5]) + ": " + str(x_count))
    f.write("\n")
    f.write("     " + str(class_name[6]) + ": " + str(b_count))
    f.write("\n")
    f.write("     " + str(class_name[7]) + ": " + str(y_count))
    f.write("\n")
    f.write("     " + str(class_name[8]) + ": " + str(h_count))
    f.write("\n")
    f.write("     " + str(class_name[9]) + ": " + str(hj_count))  # 修改点

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