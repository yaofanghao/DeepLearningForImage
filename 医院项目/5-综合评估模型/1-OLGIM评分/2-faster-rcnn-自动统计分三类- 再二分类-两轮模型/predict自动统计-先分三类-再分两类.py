# 2023.4.17 @yaofanghao
# 两阶段模型
# 先预测三分类 0-1 / 2 / 3
# 再对2和3 重新分类，预测二分类模型 2 / 3
# 删除了自动生成每张图片预测结果的 predict_result.txt

import numpy
from PIL import Image
import os
from frcnn_3class import FRCNN_3class
from frcnn_2class import FRCNN_2class

#  ##########  设置区域  ###########
dir_origin_path = "test/"  # 输入图片文件夹路径

if __name__ == "__main__":

    dir_save_path = "img_out"
    all_save_path_0 = str(dir_save_path) + "_0-1/"
    all_save_path_2 = str(dir_save_path) + "_2/"
    all_save_path_3 = str(dir_save_path) + "_3/"
    all_save_path_none = str(dir_save_path) + "_none/"
    if not os.path.exists(all_save_path_0):
        os.makedirs(all_save_path_0)
    if not os.path.exists(all_save_path_2):
        os.makedirs(all_save_path_2)
    if not os.path.exists(all_save_path_3):
        os.makedirs(all_save_path_3)
    if not os.path.exists(all_save_path_3):
        os.makedirs(all_save_path_3)
    if not os.path.exists(all_save_path_none):
        os.makedirs(all_save_path_none)

    # 统计识别为各类的个数
    num0 = 0
    num2 = 0
    num3 = 0
    none = 0

    img_names = os.listdir(dir_origin_path)
    # img_names.sort(key=lambda x:int(x.split('.')[0]))  # 按照1，2，3顺序读图片
    for img_name in img_names:
        if img_name.lower().endswith(
                ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            image_path = os.path.join(dir_origin_path, img_name)
            image = Image.open(image_path)
            print(img_name)

            # 三分类模型预测
            frcnn_3class = FRCNN_3class()
            r_image, out_scores, out_classes, _, _, _, _ = frcnn_3class.detect_image(image)

        # -----------------------------------------------------------------------------------------------#
            print(out_scores)
            print(out_classes)
            out_scores = numpy.around(out_scores, 3)

            if out_scores[0] == 0:  # 2023.3.2 解决了部分图片non-iterable的错误问题
                none += 1
                r_image.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")),
                             quality=95, subsampling=0)
                del frcnn_3class

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
                out_scores_max = round(out_scores_max, 4)   # 小数点后2位
                a = out_classes
                class_max_confidence = a[locat]  # 最大值位置的类别
                print(class_max_confidence)

                if class_max_confidence == 0:
                    class_max_confidence = '0-1'
                    num0 += 1
                    r_image.save(os.path.join(all_save_path_0, img_name.replace(".jpg", ".png")),
                                 quality=95, subsampling=0)
                    del frcnn_3class

                # 2023.4.17 修改，增加模型二阶段判断过程：
                # 如果三分类模型frcnn_3class 预测出最大为 2 / 3
                # 则对2分和3分用二分类模型重新进行分类
                else:
                    # 注意！这里 detect_image 输入参数是 image_copy
                    # 是对原图像的备份画框
                    # 而不是再一阶段模型已画框的基础上再画框！
                    del frcnn_3class
                    # del image
                    frcnn_2class = FRCNN_2class()
                    image_copy_path = os.path.join(dir_origin_path, img_name)
                    image_copy = Image.open(image_copy_path)
                    print(image_copy_path)

                    r_image_2class, out_scores_2class, out_classes_2class, top, right, left, bottom \
                        = frcnn_2class.detect_image(image_copy)

                    print(out_scores_2class)
                    print(out_classes_2class)
                    out_scores_2class = numpy.around(out_scores_2class, 3)
                    print(out_scores_2class)

                    if out_scores_2class[0] == 0:
                        none += 1
                        r_image_2class.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")),
                                            quality=95, subsampling=0)

                    if (out_scores_2class.size != 0) & (out_scores_2class[0] > 0):
                        #  ############### 找到置信度最大的类别的算法 ############
                        num = 0
                        t_2class = out_scores_2class
                        class2 = numpy.array([0])
                        class3 = numpy.array([0])
                        for i in out_classes_2class:
                            if i == 0:
                                class2 = numpy.append(class2, t_2class[num])
                            if i == 1:
                                class3 = numpy.append(class3, t_2class[num])
                            num += 1
                        class2_max = numpy.max(class2)
                        class2_max = round(class2_max, 4)
                        class3_max = numpy.max(class3)
                        class3_max = round(class3_max, 4)
                        locat_2class = out_scores_2class.argmax(axis=None, out=None)  # 找最大值位置
                        out_scores_2class_max = out_scores_2class.max()
                        out_scores_2class_max = round(out_scores_2class_max, 4)  # 小数点后2位
                        a = out_classes_2class
                        class_max_confidence_2class = a[locat_2class]  # 最大值位置的类别
                        print(class_max_confidence_2class)

                        if class_max_confidence_2class == 0:
                            class_max_confidence_2class = '2'
                            num2 += 1
                            r_image_2class.save(os.path.join(all_save_path_2, img_name.replace(".jpg", ".png")),
                                                quality=95, subsampling=0)
                        if class_max_confidence_2class == 1:
                            class_max_confidence_2class = '3'
                            num3 += 1
                            r_image_2class.save(os.path.join(all_save_path_3, img_name.replace(".jpg", ".png")),
                                                quality=95, subsampling=0)
                    del frcnn_2class

    # -----------------------------------------------------------------------------------------------#
    rate_0_1 = (num0 / (num0+num2+num3+none)) * 100
    rate_2 = (num2 / (num0+num2+num3+none)) * 100
    rate_3 = (num3 / (num0+num2+num3+none)) * 100
    rate_none = (none / (num0 + num2 + num3 + none)) * 100

    print("识别为0-1分：", num0)
    print("识别为2分：", num2)
    print("识别为3分：", num3)
    print("无结果：", none)
    print("识别为0-1分的比例：", str(rate_0_1) + '%')
    print("识别为2分的比例：", str(rate_2) + '%')
    print("识别为3分的比例：", str(rate_3) + '%')
    print("无结果的比例：", str(rate_none) + '%')

    f = open(os.path.join(os.getcwd(), 'predict_report.txt'), 'a')
    f.write("识别为0-1分：" + str(num0))
    f.write("\r")
    f.write("识别为2分：" + str(num2))
    f.write("\r")
    f.write("识别为3分：" + str(num3))
    f.write("\r")
    f.write("无结果：" + str(none))
    f.write("\r")
    f.write("识别为0分的比例：" + str(rate_0_1) + '%')
    f.write("\r")
    f.write("识别为2分的比例：" + str(rate_2) + '%')
    f.write("\r")
    f.write("识别为3分的比例：" + str(rate_3) + '%')
    f.write("\r")
    f.write("无结果的比例：" + str(rate_none) + '%')
    f.write("\r")
    f.close()
