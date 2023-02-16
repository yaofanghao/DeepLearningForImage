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

output_dir = "./output"
jpg_dir = "./JPEGImages"
png_dir = "./SegmentationClass"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(jpg_dir):
    os.makedirs(jpg_dir)
if not os.path.exists(png_dir):
    os.makedirs(png_dir)

def json_to_dataset():
    image_num = 0
    count = os.listdir("./before/")
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
    count = os.listdir("./before/")
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

if __name__ == '__main__':
    json_to_dataset()
    get_jpg_and_png()