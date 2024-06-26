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
    #-------------------------------------------------------------------------#
    #   crop                指定了是否在单张图片预测后对目标进行截取
    #   count               指定了是否进行目标的计数
    #   crop、count仅在mode='predict'时有效
    #-------------------------------------------------------------------------#
    crop            = False
    count           = False
    #-------------------------------------------------------------------------#
    #   dir_origin_path     指定了用于检测的图片的文件夹路径
    #   dir_save_path       指定了检测完图片的保存路径
    #   
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    #-------------------------------------------------------------------------#
    dir_origin_path = "img/"
    dir_save_path   = "img_out"

    # 创建图片输出的文件夹
    dir_save_path_fail_output = "img_out_fail/"
    all_save_path_allNEO = str(dir_save_path) + "_all_CIM/"
    all_save_path_allNONNEO = str(dir_save_path) + "_all_IIM/"

    if not os.path.exists(dir_save_path_fail_output):
        os.makedirs(dir_save_path_fail_output)
    if not os.path.exists(all_save_path_allNEO):
        os.makedirs(all_save_path_allNEO)
    if not os.path.exists(all_save_path_allNONNEO):
        os.makedirs(all_save_path_allNONNEO)

    # 统计识别和未识别图片个数
    fail = 0
    num1 = 0
    num2 = 0

    img_names = os.listdir(dir_origin_path)

    # 存放修改后的分数的numpy
    out_scores_new = numpy.array([])

    for img_name in tqdm(img_names):
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
            # filename = int(filename)
            # print(img_name)
            # print(filename)
            # out_scores_size = out_scores.numpy().size
            # print(out_scores.numpy())
            # print(out_scores.numpy().max()) # 这句不能有，会报错

            if out_scores.size != 0:
                ################ 找到置信度最大的类别的算法 ############
                num = 0
                t = out_scores
                tempNEO = numpy.array([0])
                tempNONNEO = numpy.array([0])

                for i in out_classes:
                    if i == 0:
                        tempNEO = numpy.append(tempNEO, t[num])
                    if i == 1:
                        tempNONNEO = numpy.append(tempNONNEO, t[num])
                    num += 1

                tempNEO_max = numpy.max(tempNEO)
                tempNEO_max=round(tempNEO_max, 4)
                tempNONNEO_max = numpy.max(tempNONNEO)
                tempNONNEO_max = round(tempNONNEO_max, 4)
                print(tempNEO_max)
                print(tempNONNEO_max)

                locat = out_scores.argmax(axis=None, out=None)  # 找最大值位置
                # print(locat)
                out_scores_max = out_scores.max()
                out_scores_max =round(out_scores_max,4)
                # print("小数后两位")
                # print(out_scores_max)
                # print(type(out_scores.numpy()))
                # print(out_classes.numpy())
                a = out_classes
                class1 = a[locat]  # 最大值位置的类别
                print(class1)
                # print(type(out_classes.numpy()))
                # out_classes = out_classes.numpy().size
                # print(out_classes.numpy())

            # -----------------------------------------------------------------------------------------------#
                # 判断语句
                flag3 = (0 in a) & (1 not in a)  # 全为0
                flag4 = (1 in a) & (0 not in a)  # 全为1
                flag5 = (1 in a) & (0 in a)  # 0和1 都有

                # 如果全为0
                if flag3:
                    num1 += 1
                    r_image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

                # 如果全为1
                if flag4:
                    num2 += 1
                    r_image.save(os.path.join(all_save_path_allNONNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

                # 如果同时有0和1
                if flag5:
                    if(class1 ==0 ):
                        r_image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),  quality=95, subsampling=0)
                        num1 += 1
                    if(class1 == 1 ):
                        num2+=1
                        r_image.save(os.path.join(all_save_path_allNONNEO,img_name.replace(".jpg", ".png")),   quality=95, subsampling=0)

            # 没有识别出任何一个框
            else:
                    r_image.save(os.path.join(dir_save_path_fail_output, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)
                    fail += 1

    print("识别为CIM：")
    print(num1)
    print("识别为IIM：")
    print(num2)
    print("无结果：")
    print(fail)
    print("识别为CIM的比例：")
    print(str((num1 / (num1+num2+fail))*100) + '%')
    print("识别为IIM的比例：")
    print(str((num2 / (num1+num2+fail))*100) + '%')

