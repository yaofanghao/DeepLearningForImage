# 2023.3.17 add
# 2023.3.19 update
# 根据新的计算方法， 计算0-1分输出的概率值 每张图最终只输出一个数值表示0-1分的概率 
# 用于绘制ROC

import numpy
from PIL import Image
import os
from frcnn import FRCNN

def softmax(x):
    x = numpy.where(x==0, -10, x)  # 0的时候，视为一个极小的值exp计算为一个很小的值
    row_max = numpy.max(x)
    # 每行元素都需要减去对应的最大值，否则求exp(x)会溢出，导致inf情况
    x = x - row_max
    x_exp = numpy.exp(x)
    x_sum = numpy.sum(x_exp)
    s = x_exp / x_sum
    s = numpy.around(s, 6)
    return s
 
if __name__ == "__main__":
    frcnn = FRCNN()

    dir_origin_path = "3/"
    dir_save_path = "img_out"

    # 存放全部图片预测结果数据的txt
    f1 = open(os.path.join(os.getcwd(), 'result_predict.txt'), 'a')

    # 存放softmax转换后的预测结果数据的txt
    f_softmax = open(os.path.join(os.getcwd(), 'result_softmax.txt'), 'a')

    # 存放经过新的计算方法得到新分数的txt
    f_new_scores = open(os.path.join(os.getcwd(), 'result_new_scores_0_1.txt'), 'a')

    # 创建图片输出的文件夹
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

    # 存放修改后的分数的numpy
    out_scores_new = numpy.array([])

    for img_name in img_names:
        if img_name.lower().endswith(
                ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            image_path = os.path.join(dir_origin_path, img_name)
            image = Image.open(image_path)
            print("名字是：------------------------------")
            print(img_name)

            # 修改detect_image 的返回值
            r_image, out_scores, out_classes, top, right, left, bottom = frcnn.detect_image(image)

            filename, extension = os.path.splitext(img_name)

            out_scores_size = out_scores.size
            # print('------------------')
            print(out_scores)
            print(out_classes)
            test1 = out_classes
            test1 = numpy.asarray(test1, dtype=int)
            out_scores = numpy.around(out_scores, 6)

            if out_scores[0] == 0:  # 2023.3.2 解决了部分图片non-iterale的错误问题
                none += 1
                r_image.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")), quality=95,
                             subsampling=0)
                f1.write(str(img_name) + "  ：none")
                f1.write("\r")
                f_softmax.write(str(img_name) + "  ：none")
                f_softmax.write("\r")
                
                # 情况1
                new_score = 0
                f_new_scores.write(str(img_name) + " " + str(new_score))
                f_new_scores.write("\r")

            if (out_scores.size != 0) & (out_scores[0] > 0):
                ################ 找到置信度最大的类别的算法 ############
                num = 0
                t = out_scores
                class0 = numpy.array([0])
                class2 = numpy.array([0])
                class3 = numpy.array([0])

                for i in out_classes:
                    if i == 0:  # 0-1分
                        class0 = numpy.append(class0, t[num])
                    if i == 1:  # 2分
                        class2 = numpy.append(class2, t[num])
                    if i == 2:  # 3分
                        class3 = numpy.append(class3, t[num])
                    num += 1

                # 得到各类别分数的最大值 非常重要！
                class0_max = numpy.max(class0)
                class0_max = round(class0_max, 6)
                class2_max = numpy.max(class2)
                class2_max = round(class2_max, 6)
                class3_max = numpy.max(class3)
                class3_max = round(class3_max, 6)

                # 计算三个类别最大分数输出的softmax值
                softmax_output = softmax(numpy.array([class0_max, class2_max, class3_max]))
                print(softmax_output)
                f_softmax.write(str(img_name) + "  三个类别最大分数经过softmax后的分数为： " )
                f_softmax.write(str(softmax_output[0]))
                f_softmax.write("  ")
                f_softmax.write(str(softmax_output[1]))
                f_softmax.write("  ")
                f_softmax.write(str(softmax_output[2]))
                f_softmax.write("\r")
                softmax_output_max = softmax_output.max()
                softmax_output_max = round(softmax_output_max,6)

                locat = out_scores.argmax(axis=None, out=None)  # 找最大值位置
                out_scores_max = out_scores.max()
                out_scores_max = round(out_scores_max, 6)
                a = out_classes
                class_max_confidence = a[locat]  # 最大值位置的类别
                print(class_max_confidence)

                # 2022.12.13 修改了准确率判定准则
                if class_max_confidence == 0:
                    if class0_max - class2_max <= 0.3:
                        class_max_confidence = '2'
                        num2 += 1
                        r_image.save(os.path.join(all_save_path_2, img_name.replace(".jpg", ".png")), quality=95,
                                     subsampling=0)
                    else:
                        class_max_confidence = '0-1'
                        num0 += 1
                        r_image.save(os.path.join(all_save_path_0, img_name.replace(".jpg", ".png")), quality=95,
                                     subsampling=0)
                if class_max_confidence == 1:
                    class_max_confidence = '2'
                    num2 += 1
                    r_image.save(os.path.join(all_save_path_2, img_name.replace(".jpg", ".png")), quality=95,
                                 subsampling=0)
                if class_max_confidence == 2:
                    class_max_confidence = '3'
                    num3 += 1
                    r_image.save(os.path.join(all_save_path_3, img_name.replace(".jpg", ".png")), quality=95,
                                 subsampling=0)

                f1.write(str(img_name) + "  三个类别最大分数原始值为： ")
                f1.write(str(class0_max))
                f1.write("  ")
                f1.write(str(class2_max))
                f1.write("  ")
                f1.write(str(class3_max))
                f1.write("\r")

                # 2023.3.19 2.0版
                # 情况2
                if (class0_max==0) & (class2_max>0) & (class3_max==0):
                    new_score = 0.2-0.2*class2_max                    

                # 情况3
                if (class0_max==0) & (class2_max==0) & (class3_max>0):
                    new_score = 0.2-0.2*class3_max
                
                # 情况4
                if (class0_max==0) & (class2_max>0) & (class3_max>0):
                    new_score = 0

                # 情况5\6\7
                if (class0_max>0) & ((class2_max>0) | (class3_max>0)):
                    new_score = 0.2+0.5*softmax_output[0]

                # 情况8
                if (class0_max>0) & (class2_max==0) & (class3_max==0):
                    new_score = class0_max

                new_score = round(new_score,6)
                f_new_scores.write(str(img_name) + " " + str(new_score))
                f_new_scores.write("\r")


    # # -----------------------------------------------------------------------------------------------#
    print("识别为0-1分：")
    print(num0)
    print("识别为2分：")
    print(num2)
    print("识别为3分：")
    print(num3)
    print("无结果：")
    print(none)
    print("识别为0-1分的比例：")
    print(str((num0 / (num0 + num2 + num3 + none)) * 100) + '%')
    print("识别为2分的比例：")
    print(str((num2 / (num0 + num2 + num3 + none)) * 100) + '%')
    print("识别为3分的比例：")
    print(str((num3 / (num0 + num2 + num3 + none)) * 100) + '%')
    print("无结果的比例：")
    print(str((none / (num0 + num2 + num3 + none)) * 100) + '%')

    f1.close()
    f_softmax.close()
    f_new_scores.close()

    f = open(os.path.join(os.getcwd(), 'report_predict.txt'), 'a')
    f.write("识别为0-1分：" + str(num0))
    f.write("\r")
    f.write("识别为2分：" + str(num2))
    f.write("\r")
    f.write("识别为3分：" + str(num3))
    f.write("\r")
    f.write("无结果：" + str(none))
    f.write("\r")
    f.write("识别为0分的比例：" + str((num0 / (num0 + num2 + num3 + none)) * 100) + '%')
    f.write("\r")
    f.write("识别为2分的比例：" + str((num2 / (num0 + num2 + num3 + none)) * 100) + '%')
    f.write("\r")
    f.write("识别为3分的比例：" + str((num3 / (num0 + num2 + num3 + none)) * 100) + '%')
    f.write("\r")
    f.write("无结果的比例：" + str((none / (num0 + num2 + num3 + none)) * 100) + '%')
    f.write("\r")
    f.close()

