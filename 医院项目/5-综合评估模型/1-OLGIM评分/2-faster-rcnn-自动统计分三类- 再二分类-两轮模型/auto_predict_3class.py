"""

    -*- coding: utf-8 -*-
    @Author  : yaofanghao
    @Last edit time    : 2023/4/18 11:20
    @File    : auto_predict_3class.py
    @Software: PyCharm 
    
"""
import numpy
from PIL import Image
import os, sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
from frcnn_3class import FRCNN_3class
from tqdm import tqdm

def predict_3class(dir_origin):
    frcnn_3class = FRCNN_3class()

    dir_origin_path = str(dir_origin) + "/"
    dir_save_path = "img_out"
    all_save_path_0 = str("predict_result_") + str(dir_origin) + "/" + str(dir_save_path) + "_0-1/"
    all_save_path_none = str("predict_result_") + str(dir_origin) + "/" + str(dir_save_path) + "_none/"
    dir_save_path_temp = str("predict_result_") + str(dir_origin) + "/" + str(dir_save_path) + "_temp/"
    if not os.path.exists(all_save_path_0):
        os.makedirs(all_save_path_0)
    if not os.path.exists(all_save_path_none):
        os.makedirs(all_save_path_none)
    if not os.path.exists(dir_save_path_temp):
        os.makedirs(dir_save_path_temp)

    img_names = os.listdir(dir_origin_path)
    # img_names.sort(key=lambda x:int(x.split('.')[0]))  # 按照1，2，3顺序读图片
    for img_name in tqdm(img_names):
        image_path = os.path.join(dir_origin_path, img_name)
        image = Image.open(image_path)
        # print(img_name)

        # 三分类模型预测
        r_image, out_scores, out_classes, _, _, _, _ = frcnn_3class.detect_image(image)
        # print(out_scores)
        # print(out_classes)
        out_scores = numpy.around(out_scores, 3)

        if out_scores[0] == 0:  # 2023.3.2 解决了部分图片non-iterable的错误问题
            r_image.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")),
                         quality=95, subsampling=0)

        if (out_scores.size != 0) & (out_scores[0] > 0):
            #  ############### 找到置信度最大的类别的算法 ############
            num = 0
            t_3class = out_scores
            class0 = numpy.array([0])
            class2 = numpy.array([0])
            class3 = numpy.array([0])
            for i in out_classes:
                if i == 0:
                    class0 = numpy.append(class0, t_3class[num])
                if i == 1:
                    class2 = numpy.append(class2, t_3class[num])
                if i == 2:
                    class3 = numpy.append(class3, t_3class[num])
                num += 1
            class0_max = numpy.max(class0)
            class0_max = round(class0_max, 4)
            class2_max = numpy.max(class2)
            class2_max = round(class2_max, 4)
            class3_max = numpy.max(class3)
            class3_max = round(class3_max, 4)
            locat = out_scores.argmax(axis=None, out=None)  # 找最大值位置
            out_scores_max = out_scores.max()
            out_scores_max = round(out_scores_max, 4)  # 小数点后2位
            a = out_classes
            class_max_confidence = a[locat]  # 最大值位置的类别
            # print(class_max_confidence)

            if class_max_confidence == 0:
                class_max_confidence = '0-1'
                r_image.save(os.path.join(all_save_path_0, img_name.replace(".jpg", ".png")),
                             quality=95, subsampling=0)
            else:
                # 预测为2/3的 存放至temp文件夹，保存的是原图
                image_copy = Image.open(image_path)
                image_copy.save(os.path.join(dir_save_path_temp, img_name.replace(".jpg", ".png")),
                                quality=95, subsampling=0)

if __name__ == "__main__":
    # 设置传入参数 ： 输入图片文件夹名称 不带斜杠
    # 默认为 test 文件夹
    # 示例：如果要预测文件夹 dir1
    # 则在终端输入： python uto_predict_3class.py dir1
    if len(sys.argv) == 1:
        dir_origin = "test"
    else:  # 手动传入待预测文件夹名称
        dir_origin = sys.argv[1]
    predict_3class(dir_origin)