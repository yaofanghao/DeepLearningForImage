import time
import cv2
import numpy
from PIL import Image
import os
from tqdm import tqdm

from frcnn import FRCNN

if __name__ == "__main__":
    frcnn = FRCNN()
    mode = "dir_predict"
    dir_origin_path = "jpg0-1/"
    dir_save_path = "img_out"

    if mode == "dir_predict":
        # -----------------------------------#
        # !!! 唯一需要手动设置的地方：confidence_num
        confidence_num = 0.05
        confidence_down = confidence_num
        confidence_up = confidence_down + 0.1

        # 存放全部图片预测结果数据的txt
        f1 = open(os.path.join(os.getcwd(), 'predict_result.txt'), 'a')

        if confidence_down < 0.92:
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
                    r_image, out_scores, out_classes,top,right, left,bottom= frcnn.detect_image(image)

                    # 分离名字 进行格式转换
                    filename, extension = os.path.splitext(img_name)
                # -----------------------------------------------------------------------------------------------#
                    out_scores_size = out_scores.size
                    # print('------------------')
                    print(out_scores)
                    print(out_classes)
                    f1.write(img_name)
                    f1.write("\r")
                    test1 = out_classes
                    test1 = test1.astype(int)
                    f1.write("预测的类别为：")
                    f1.write("\r")
                    numpy.savetxt(f1,test1)
                    f1.write("对应的置信度分数为：")
                    f1.write("\r")
                    numpy.savetxt(f1,out_scores)
                    # print(out_scores.max()) # 这句不能有，会报错
                    # -----------------------------------------------------------------------------------------------------

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
                            if i == 2:
                                class2 = numpy.append(class2, t[num])
                            if i == 3:
                                class3 = numpy.append(class3, t[num])
                            num += 1

                        class0_max = numpy.max(class0)
                        class0_max=round(class0_max, 4)
                        class2_max = numpy.max(class2)
                        class2_max=round(class2_max, 4)
                        class3_max = numpy.max(class3)
                        class3_max=round(class3_max, 4)
                        # print(class0_max)
                        # print(class1_max)
                        # print(class2_max)
                        # print(class3_max)

                        locat = out_scores.argmax(axis=None, out=None)  # 找最大值位置
                        # print(locat)
                        out_scores_max = out_scores.max()
                        out_scores_max =round(out_scores_max,4)   # 小数点后2位
                        # print("小数后两位")
                        # print(out_scores_max)
                        # print(type(out_scores))
                        # print(out_classes.numpy())
                        a = out_classes
                        class_max_confidence = a[locat]  # 最大值位置的类别 可能值为： 0\1\2\3
                        print(class_max_confidence)
                        f1.write("置信度分数最大的类别为："+str(class_max_confidence)+"分")
                        f1.write("\r")
                        f1.write("分数为："+str(out_scores_max))
                        f1.write("\r")
                        # print(type(out_classes))
                        # out_classes = out_classes.size
                        # print(out_classes)

                    # -----------------------------------------------------------------------------------------------#
                        # 按照置信度最大类别，分至五个文件夹 0\1\2\3\none
                        if class_max_confidence == 0:
                            num0 += 1
                            r_image.save(os.path.join(all_save_path_0, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
                        if class_max_confidence == 2:
                            num2 += 1
                            r_image.save(os.path.join(all_save_path_2, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
                        if class_max_confidence == 3:
                            num3 += 1
                            r_image.save(os.path.join(all_save_path_3, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

                    # -----------------------------------------------------------------------------------------------#
                    else: # 没有识别出任何一个框
                        none += 1
                        r_image.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)

            # # -----------------------------------------------------------------------------------------------#
            # 打印出来结果
            print("识别为0-1分：")
            print(num0)
            print("识别为2分：")
            print(num2)
            print("识别为3分：")
            print(num3)
            print("无结果：")
            print(none)

            print("识别为0-1分的比例：")
            print(str((num0 / (num0+num2+num3+none))*100) + '%')
            print("识别为2分的比例：")
            print(str((num2 / (num0+num2+num3+none))*100) + '%')
            print("识别为3分的比例：")
            print(str((num3 / (num0+num2+num3+none))*100) + '%')
            print("无结果的比例：")
            print(str((none / (num0+num2+num3+none))*100) + '%')

            #----------------------------------------------------------------------------------------------#
            # 对应预测结果存至txt中
            ####   getcwd()  当前路径
            f1.close()
            f = open(os.path.join(os.getcwd(), 'predict_report.txt'), 'a')
            f.write("识别为0-1分：" + str(num0))
            f.write("\r")
            f.write("识别为2分：" + str(num2))
            f.write("\r")
            f.write("识别为3分：" + str(num3))
            f.write("\r")
            f.write("无结果：" + str(none))
            f.write("\r")
            f.write("识别为0分的比例：" + str((num0 / (num0+num2+num3+none))*100) + '%')
            f.write("\r")
            f.write("识别为2分的比例：" + str((num2 / (num0+num2+num3+none))*100) + '%')
            f.write("\r")
            f.write("识别为3分的比例：" + str((num3 / (num0+num2+num3+none))*100) + '%')
            f.write("\r")
            f.write("无结果的比例：" + str((none / (num0+num2+num3+none))*100) + '%')
            f.write("\r")
            f.close()

            confidence_down = confidence_down + 0.1
            confidence_up = confidence_down + 0.1
            #######################以上为修改部分##########################


    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps' or 'dir_predict'.")
