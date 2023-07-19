# 2023.2.15 @ yaofanghao
# json格式数据集制作的一步到位版
# 2023.2.16 解决了一些png和JPG格式后缀的问题

import PIL.Image
import json
import os
import os.path as osp
import warnings
import numpy as np
from PIL import Image
import yaml
from labelme import utils
import base64
from tqdm import tqdm

origin_dir = "./before/"

output_dir = "./output"
jpg_dir = "./JPEGImages"
png_dir = "./SegmentationClass"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(jpg_dir):
    os.makedirs(jpg_dir)
if not os.path.exists(png_dir):
    os.makedirs(png_dir)

# 待统计图片的标签类别设置
class_name = ["duoyuwu", "yanghuawu", "gubo", "huashang",
              "qipi", "xiuban", "aokeng", "hanjiequexian"]   # 修改点

# 统计模式设置
# count_mode 为 0
#   一张图中如果有多个相同类别的标注，在统计中对这些每个标注都会加1
# count_mode 为 1
#   对一张图中的多个相同类别的标注只加一次1
count_mode = 1

def json_to_dataset():
    image_num = 0
    count = os.listdir(origin_dir)
    for i in range(0, len(count)):
        path = os.path.join("./before", count[i])
        png_name = count[i].split('.')[0]

        if os.path.isfile(path) and path.endswith('json'):
            data = json.load(open(path))
            if data['imageData']:
                imageData = data['imageData']
            else:
                imagePath = os.path.join(os.path.dirname(path), data['imagePath'])
                with open(imagePath, 'rb') as f:
                    imageData = f.read()
                    imageData = base64.b64encode(imageData).decode('utf-8')
            img = utils.img_b64_to_arr(imageData)
            label_name_to_value = {'_background_': 0}
            for shape in data['shapes']:
                label_name = shape['label']
                if label_name in label_name_to_value:
                    label_value = label_name_to_value[label_name]
                else:
                    label_value = len(label_name_to_value)
                    label_name_to_value[label_name] = label_value

            # label_values must be dense
            label_values, label_names = [], []
            for ln, lv in sorted(label_name_to_value.items(), key=lambda x: x[1]):
                label_values.append(lv)
                label_names.append(ln)
            assert label_values == list(range(len(label_values)))

            lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)
            captions = ['{}: {}'.format(lv, ln)
                        for ln, lv in label_name_to_value.items()]
            lbl_viz = utils.draw_label(lbl, img, captions)
            out_dir = osp.basename(count[i]).replace('.', '_')
            out_dir = osp.join(osp.dirname(count[i]), out_dir)
            out_dir = osp.join("output", out_dir)

            if not osp.exists(out_dir):
                os.mkdir(out_dir)
            PIL.Image.fromarray(img).save(osp.join(out_dir, 'img.png'))
            utils.lblsave(osp.join(out_dir, 'label.png'), lbl)
            PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))
            PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, png_name+'_viz'+'.png'))
            with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
                for lbl_name in label_names:
                    f.write(lbl_name + '\n')

            warnings.warn('info.yaml is being replaced by label_names.txt')
            info = dict(label_names=label_names)
            with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
                yaml.safe_dump(info, f, default_flow_style=False)
            image_num += 1
            print(image_num, 'Saved to: %s' % out_dir)
    print("完成json to dataset步骤!")

def get_jpg_and_png():
    # 读取原文件夹
    count = os.listdir(origin_dir)
    for i in range(0, len(count)):
        # 如果里的文件以jpg结尾
        # 则寻找它对应的png
        if count[i].endswith("jpg") or count[i].endswith("JPG"):
            if count[i].endswith("JPG"):
                count[i].replace("JPG", "jpg")
            path = os.path.join("./before", count[i])
            img = Image.open(path)

            # 这句convert如果不加，读取png图片会报错
            # raise OSError(f"cannot write mode {im.mode} as JPEG") from e  OSError: cannot write mode RGBA as JPEG
            img = img.convert('RGB')

            img.save(os.path.join("./JPEGImages", count[i]))

            # 找到对应的png
            path = "./output/" + count[i].split(".")[0] + "_json/label.png"
            img = Image.open(path)

            # 找到全局的类
            class_txt = open("./before/class_name.txt", "r")
            class_name = class_txt.read().splitlines()
            # ["bk","cat","dog"]
            # 打开json文件里面存在的类，称其为局部类
            with open("./output/" + count[i].split(".")[0] + "_json/label_names.txt", "r") as f:
                names = f.read().splitlines()
                # ["bk","dog"]
                new = Image.new("RGB", [np.shape(img)[1], np.shape(img)[0]])
                for name in names:
                    # index_json是json文件里存在的类，局部类
                    index_json = names.index(name)
                    # index_all是全局的类
                    index_all = class_name.index(name)
                    # 将局部类转换成为全局类
                    new = new + np.expand_dims(index_all * (np.array(img) == index_json), -1)
                    print("ok")
            new = Image.fromarray(np.uint8(new))
            if count[i].endswith("jpg") :
                new.save(os.path.join("./SegmentationClass", count[i].replace("jpg", "png")))
            if count[i].endswith("JPG"):
                new.save(os.path.join("./SegmentationClass", count[i].replace("JPG", "png")))

            print(np.max(new), np.min(new))
    print("完成get_jpg_and_png步骤!")

def count_json_label():
    base_path = "before/"
    filelist = os.listdir(base_path)

    dir_count = 0
    d_count, a_count, q_count, c_count, g_count, x_count, b_count, y_count, h_count, hj_count \
        = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0   # 修改点
    f = open(os.path.join(os.getcwd(), 'json_class_result_mode' + str(count_mode) + '.txt'), 'a')

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


if __name__ == '__main__':
    json_to_dataset()
    get_jpg_and_png()  # 生成数据集的jpg和png文件
    count_json_label()  # 批量统计json文件类别和个数