# 2023.2.16- 综合评估代码修改中 @yaofanghao
# 胃窦取每个图片输出最大分数，计算平均分数并四舍五入为A
# 胃体取每个图片输出最大分数，计算平均分数并四舍五入为B
#   平均值 [0, 1.5) ->1  [1.5, 2.5) ->2  [2.5,3] ->3
# A和B再进行OLGIM综合评估，得到结果为 0-1 / 2 / high
# update 2023.4.14

import numpy
from PIL import Image
import os
import warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
warnings.filterwarnings("ignore")
from tqdm import tqdm
from decimal import Decimal
from frcnn import FRCNN

base_dir_path = "img/沈乔林/"
dir_weidou_path = str(base_dir_path) + "胃窦"
dir_weiti_path = str(base_dir_path) + "胃体"
dir_save_path = str(base_dir_path) + "img_out"
all_save_path_0 = str(dir_save_path) + "_0-1/"
all_save_path_2 = str(dir_save_path) + "_2/"
all_save_path_high = str(dir_save_path) + "_high/"
all_save_path_none = str(dir_save_path) + "_none/"
if not os.path.exists(all_save_path_0):
    os.makedirs(all_save_path_0)
if not os.path.exists(all_save_path_2):
    os.makedirs(all_save_path_2)
if not os.path.exists(all_save_path_high):
    os.makedirs(all_save_path_high)
if not os.path.exists(all_save_path_none):
    os.makedirs(all_save_path_none)

if __name__ == "__main__":
    frcnn = FRCNN()

############ ------------ 预测胃窦文件夹中所有图片
    img_names = os.listdir(dir_weidou_path)

    # class_max_confidence_weidou 是存放每张图胃窦预测分数的numpy
    class_max_confidence_weidou = numpy.array([],dtype=int)
    for img_name in img_names:
        print("预测中... ", dir_weidou_path, img_name)
        image_path = os.path.join(dir_weidou_path, img_name)
        image = Image.open(image_path)

        r_image, out_scores, out_classes,top,right, left,bottom= frcnn.detect_image(image)
        filename, extension = os.path.splitext(img_name)
        out_scores_size = out_scores.size
        # print("out_scores:", out_scores)
        # print("out_classes", out_classes)
        test1 = out_classes
        test1 = numpy.asarray(test1, dtype=int)
        out_scores = numpy.around(out_scores,3)

        if out_scores.size != 0:
            ################ 找到置信度最大的类别的算法 ############
            num = 0
            t = out_scores
            class0 = numpy.array([0])
            class2 = numpy.array([0])
            class3 = numpy.array([0])
            for i in out_classes:
                if i == 0:
                    class0 = numpy.append(class0, t[num])
                if i == 1:
                    class2 = numpy.append(class2, t[num])
                if i == 2:
                    class3 = numpy.append(class3, t[num])
                num += 1
            class0_max = numpy.max(class0)
            class0_max=round(class0_max, 4)
            class2_max = numpy.max(class2)
            class2_max=round(class2_max, 4)
            class3_max = numpy.max(class3)
            class3_max=round(class3_max, 4)
            locat = out_scores.argmax(axis=None, out=None)  # 预测结果最大值的位置
            out_scores_max = out_scores.max()  # 预测结果最大值
            out_scores_max =round(out_scores_max,4)   # 小数点后4位
            a = out_classes
            class_max_confidence = a[locat]  # 预测结果最大值的位置的类别
            print("    class_max_confidence:", class_max_confidence)

            if class_max_confidence == 0:
                class_max_confidence = '0-1'
                r_image.save(os.path.join(all_save_path_0, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
                class_max_confidence_weidou = numpy.append(class_max_confidence_weidou, 1)
            if class_max_confidence == 1:
                class_max_confidence = '2'
                r_image.save(os.path.join(all_save_path_2, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
                class_max_confidence_weidou = numpy.append(class_max_confidence_weidou, 2)
            if class_max_confidence == 2:
                class_max_confidence = '3'
                class_max_confidence_weidou = numpy.append(class_max_confidence_weidou, 3)
                r_image.save(os.path.join(all_save_path_high, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
        else: # 没有识别出任何一个框
            r_image.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)

    print("胃窦的 class_max_confidence 分别为：")
    for i in range(class_max_confidence_weidou.shape[0]):
        print(class_max_confidence_weidou[i], end=' ')

    # 分析class_max_confidence_weidou，取平均值并四舍五入作为胃窦病例的最终输入结果
    weidou_average = numpy.mean(class_max_confidence_weidou,axis=0)
    weidou_average = Decimal(weidou_average).quantize(Decimal("1."), rounding="ROUND_HALF_UP")
    print("胃窦的最终分数为：", weidou_average)
    print("\n")

############ ------------ 预测胃体文件夹中所有图片
    img_names = os.listdir(dir_weiti_path)

    # class_max_confidence_weiti 是存放每张图胃体预测分数的numpy
    class_max_confidence_weiti = numpy.array([],dtype=int)
    for img_name in img_names:
        print("预测中... ", dir_weiti_path, img_name)
        image_path = os.path.join(dir_weiti_path, img_name)
        image = Image.open(image_path)

        r_image, out_scores, out_classes,top,right, left,bottom= frcnn.detect_image(image)
        filename, extension = os.path.splitext(img_name)
        out_scores_size = out_scores.size
        # print("out_scores:", out_scores)
        # print("out_classes", out_classes)
        test1 = out_classes
        test1 = numpy.asarray(test1, dtype=int)
        out_scores = numpy.around(out_scores,3)

        if out_scores.size != 0:
            ################ 找到置信度最大的类别的算法 ############
            num = 0
            t = out_scores
            class0 = numpy.array([0])
            class2 = numpy.array([0])
            class3 = numpy.array([0])
            for i in out_classes:
                if i == 0:
                    class0 = numpy.append(class0, t[num])
                if i == 1:
                    class2 = numpy.append(class2, t[num])
                if i == 2:
                    class3 = numpy.append(class3, t[num])
                num += 1
            class0_max = numpy.max(class0)
            class0_max=round(class0_max, 4)
            class2_max = numpy.max(class2)
            class2_max=round(class2_max, 4)
            class3_max = numpy.max(class3)
            class3_max=round(class3_max, 4)
            locat = out_scores.argmax(axis=None, out=None)  # 预测结果最大值的位置
            out_scores_max = out_scores.max()  # 预测结果最大值
            out_scores_max =round(out_scores_max,4)   # 小数点后4位
            a = out_classes
            class_max_confidence = a[locat]  # 预测结果最大值的位置的类别
            print("    class_max_confidence:", class_max_confidence)

            if class_max_confidence == 0:
                class_max_confidence = '0-1'
                r_image.save(os.path.join(all_save_path_0, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
                class_max_confidence_weiti = numpy.append(class_max_confidence_weiti, 1)
            if class_max_confidence == 1:
                class_max_confidence = '2'
                r_image.save(os.path.join(all_save_path_2, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
                class_max_confidence_weiti = numpy.append(class_max_confidence_weiti, 2)
            if class_max_confidence == 2:
                class_max_confidence = '3'
                class_max_confidence_weiti = numpy.append(class_max_confidence_weiti, 3)
                r_image.save(os.path.join(all_save_path_high, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
        else: # 没有识别出任何一个框
            r_image.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)

    print("胃窦的 class_max_confidence 分别为：")
    for i in range(class_max_confidence_weiti.shape[0]):
        print(class_max_confidence_weiti[i], end=' ')

    # 分析class_max_confidence_weidou，取平均值并四舍五入作为胃窦病例的最终输入结果
    weiti_average = numpy.mean(class_max_confidence_weiti,axis=0)
    weiti_average = Decimal(weiti_average).quantize(Decimal("1."), rounding="ROUND_HALF_UP")
    print("胃体的最终分数为：", weiti_average)
    print("\n")

############ ------------ 综合评估结果，输出 0-1 / 2 / high risk
    final_result = 0
    if (weidou_average==1) & (weiti_average==1):
        final_result = 1
    if (weidou_average==2) & (weiti_average==1):
        final_result = 2
    if (weidou_average==1) & (weiti_average==2):
        final_result = 2
    if (weidou_average==2) & (weiti_average==2):
        final_result = 3
    if (weidou_average==3) | (weiti_average==3):
        final_result = str("high")
    print("最终评估结果为：", str(final_result))



