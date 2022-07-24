import numpy
import tensorflow as tf
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from yolo_predict3 import YOLO
import os
from tqdm import tqdm

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# 根据修改后的置信度画图
def draw_new_scores(image,out_scores_max,left,top,right,bottom):
    label = '{:.2f}'.format(out_scores_max)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font='model_data/simhei.ttf',
                              size=np.floor(3e-2 * image.size[1] + 2).astype('int32'))
    label_size = draw.textsize(label, font)
    label = label.encode('utf-8')
    print('7.23test')
    print(label, top, left, bottom, right)

    if top - label_size[1] >= 0:
        text_origin = np.array([left, top - label_size[1]])
    else:
        text_origin = np.array([left, top + 1])

    draw.rectangle([left, top, right, bottom], outline=(255, 255, 255), width=10)
    draw.rectangle([tuple(text_origin), tuple(text_origin + label_size)], fill=(255, 0, 0))
    draw.text(text_origin, str(label, 'UTF-8'), fill=(0, 0, 0), font=font)
    del draw

# 预测批量图片
# dir_origin_path = "img/"
# dir_save_path = "img_out"
# def predict11(dir_origin_path,dir_save_path):
#     yolo = YOLO()
#
#     # -----------------------------------#
#     # !!! 唯一需要手动设置的地方：confidence_num
#     confidence_num = 0.05
#     confidence_down = confidence_num
#     confidence_up = confidence_down + 0.1
#
#     if confidence_down < 0.92:
#         # 创建输出的文件夹：全0，全1，0和1都有
#         all_save_path_allNEO = str(dir_save_path) + "_NEO/"
#         all_save_path_allNONNEO = str(dir_save_path) + "_NONNEO/"
#         dir_save_path_fail_output = "img_out_fail/"
#
#         if not os.path.exists(dir_save_path_fail_output):
#             os.makedirs(dir_save_path_fail_output)
#         if not os.path.exists(all_save_path_allNEO):
#             os.makedirs(all_save_path_allNEO)
#         if not os.path.exists(all_save_path_allNONNEO):
#             os.makedirs(all_save_path_allNONNEO)
#
#         img_names = os.listdir(dir_origin_path)
#
#         # 存放修改后的分数的numpy
#         out_scores_new = numpy.array([])
#
#         for img_name in tqdm(img_names):
#             if img_name.lower().endswith(
#                     ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
#                 image_path = os.path.join(dir_origin_path, img_name)
#                 image = Image.open(image_path)
#
#                 # 修改detect_image 的返回值
#                 out_scores, out_classes,top,right, left,bottom= yolo.detect_image(image)
#
#                 # 分离名字 进行格式转换
#                 out_scores_size = out_scores.numpy().size
#                 # print(out_scores.numpy())
#                 # print(out_scores.numpy().max()) # 这句不能有，会报错
#
#                 if out_scores.numpy().size != 0:
#                     ################ 找到置信度最大的类别的算法 ############
#                     num = 0
#                     t = out_scores
#                     tempNEO = numpy.array([0])
#                     tempNONNEO = numpy.array([0])
#
#                     for i in out_classes.numpy():
#                         if i == 0:
#                             tempNEO = numpy.append(tempNEO, t[num])
#                         if i == 1:
#                             tempNONNEO = numpy.append(tempNONNEO, t[num])
#                         num += 1
#
#                     tempNEO_max = numpy.max(tempNEO)
#                     tempNEO_max=round(tempNEO_max, 2)
#                     tempNONNEO_max = numpy.max(tempNONNEO)
#                     tempNONNEO_max = round(tempNONNEO_max, 2)
#
#                     locat = out_scores.numpy().argmax(axis=None, out=None)  # 找最大值位置
#                     out_scores_max = out_scores.numpy().max()
#                     out_scores_max =round(out_scores_max,2)   # 小数点后2位
#                     a = out_classes.numpy()
#                     class1 = a[locat]  # 最大值位置的类别
#
#                 # -----------------------------------------------------------------------------------------------#
#                     # 判断语句
#                     flag3 = (0 in a) & (1 not in a)  # 全为0
#                     flag4 = (1 in a) & (0 not in a)  # 全为1
#                     flag5 = (1 in a) & (0 in a)  # 0和1 都有
#
#                 # -----------------------------------------------------------------------------------------------#
#                     # 如果全为0（癌症），进入癌症文件夹
#                     if flag3:
#
#                         #修改全0的分数 tempNEO_max
#                         print("修改前分数：", tempNEO_max)
#                         tempNEO_max = 0.3*tempNEO_max + 0.7
#                         tempNEO_max = round(tempNEO_max, 2)
#                         print("修改后分数：", tempNEO_max)
#                         out_scores_new = numpy.append(out_scores_new, tempNEO_max)
#
#                         draw_new_scores(image,tempNEO_max, left, top, right, bottom)
#                         image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
#
#                 #-----------------------------------------------------------------------------------------------#
#                     # 如果全为1（非癌症），进入这个非癌症文件夹
#                     if flag4:
#
#                         #修改全1的分数 tempNONNEO_max
#                         print("修改前分数：", tempNONNEO_max)
#                         tempNONNEO_max = 0.3 - 0.3*tempNONNEO_max
#                         tempNONNEO_max = round(tempNONNEO_max, 2)
#                         print("修改后分数：", tempNONNEO_max)
#                         out_scores_new = numpy.append(out_scores_new, tempNONNEO_max)
#
#                         if int(top) < 0: top = 0
#                         if int(right) < 0: right = 0
#                         if int(left) < 0: left = 0
#                         if int(bottom) < 0: bottom = 0
#
#                         draw_new_scores(image,tempNONNEO_max, left, top, right, bottom)
#                         image.save(os.path.join(all_save_path_allNONNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
#
#                 # -----------------------------------------------------------------------------------------------#
#                     # 如果同时有0和1，进入这个算法
#                     if flag5:
#                         if(class1 ==0 ):
#                              # 修改分数 tempNEO_max
#                              print("修改前分数：", tempNEO_max)
#                              if tempNEO_max > 0.9:
#                                  if tempNEO_max - tempNONNEO_max < 0.1:
#                                      tempNEO_max = 0.3*tempNEO_max + 0.7
#                                  else:
#                                      tempNEO_max = 0.2 * tempNEO_max + 0.5
#                              if tempNEO_max < 0.9:
#                                  tempNEO_max = 0.5*tempNEO_max + 0.5
#                              tempNEO_max=round(tempNEO_max, 2)
#                              print("修改后分数：", tempNEO_max)
#                              out_scores_new = numpy.append(out_scores_new, tempNEO_max)
#
#                              if int(top) < 0: top = 0
#                              if int(right) < 0: right = 0
#                              if int(left) < 0: left = 0
#                              if int(bottom) < 0: bottom = 0
#
#                              draw_new_scores(image,tempNEO_max, left, top, right, bottom)
#                              image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")), quality=95,
#                                    subsampling=0)
#
#                         if(class1 == 1 ):
#                             # 修改分数 tempNONNEO_max
#                             print("修改前分数：", tempNONNEO_max)
#                             if tempNONNEO_max > 0.9:
#                                 if tempNONNEO_max - tempNEO_max < 0.1:
#                                     tempNONNEO_max = 0.2 * tempNONNEO_max + 0.3
#                                 else:
#                                     tempNONNEO_max = 0.3-0.3 * tempNONNEO_max
#                             if tempNONNEO_max < 0.9:
#                                 tempNONNEO_max = 0.5-0.5 * tempNONNEO_max
#                             tempNONNEO_max = round(tempNONNEO_max, 2)
#                             print("修改后分数：", tempNONNEO_max)
#                             out_scores_new = numpy.append(out_scores_new, tempNONNEO_max)
#
#                             if int(top) < 0: top = 0
#                             if int(right) < 0: right = 0
#                             if int(left) < 0: left = 0
#                             if int(bottom) < 0: bottom = 0
#
#                             draw_new_scores(image,tempNONNEO_max, left, top, right, bottom)
#                             image.save(os.path.join(all_save_path_allNONNEO,img_name.replace(".jpg", ".png")),   quality=95, subsampling=0)
#
#                 # -----------------------------------------------------------------------------------------------#
#                 else: # 没有识别出任何一个框
#                      out_scores_new = numpy.append(out_scores_new, 0)
#                      # draw_new_scores(image,0, 0, 0, 0, 0)  # 这句也可以不要，因为没有生成结果，直接保存原图
#                      image.save(os.path.join(dir_save_path_fail_output, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)
#
#         #----------------------------------------------------------------------------------------------#
#         confidence_down = confidence_down + 0.1
#         confidence_up = confidence_down + 0.1


# 预测单张图片


def predict11_single(image,img_name):
    yolo = YOLO()

    dir_origin_path = "img/"
    dir_save_path = "img_out"
    # -----------------------------------#
    # !!! 唯一需要手动设置的地方：confidence_num
    confidence_num = 0.05
    confidence_down = confidence_num
    confidence_up = confidence_down + 0.1

    if confidence_down < 0.92:
        # 创建输出的文件夹：全0，全1，0和1都有
        all_save_path_allNEO = str(dir_save_path) + "_NEO/"
        all_save_path_allNONNEO = str(dir_save_path) + "_NONNEO/"
        dir_save_path_fail_output = "img_out_fail/"

        if not os.path.exists(dir_save_path_fail_output):
            os.makedirs(dir_save_path_fail_output)
        if not os.path.exists(all_save_path_allNEO):
            os.makedirs(all_save_path_allNEO)
        if not os.path.exists(all_save_path_allNONNEO):
            os.makedirs(all_save_path_allNONNEO)

        # 修改detect_image 的返回值
        out_scores, out_classes, top, right, left, bottom = yolo.detect_image(image)

        if out_scores.numpy().size != 0:
            ################ 找到置信度最大的类别的算法 ############
            num = 0
            t = out_scores
            tempNEO = numpy.array([0])
            tempNONNEO = numpy.array([0])

            for i in out_classes.numpy():
                if i == 0:
                    tempNEO = numpy.append(tempNEO, t[num])
                if i == 1:
                    tempNONNEO = numpy.append(tempNONNEO, t[num])
                num += 1

            tempNEO_max = numpy.max(tempNEO)
            tempNEO_max = round(tempNEO_max, 2)
            tempNONNEO_max = numpy.max(tempNONNEO)
            tempNONNEO_max = round(tempNONNEO_max, 2)

            locat = out_scores.numpy().argmax(axis=None, out=None)  # 找最大值位置
            # out_scores_max = out_scores.numpy().max()
            # out_scores_max = round(out_scores_max, 2)  # 小数点后2位
            a = out_classes.numpy()
            class1 = a[locat]  # 最大值位置的类别

            # -----------------------------------------------------------------------------------------------#
            # 判断语句
            flag3 = (0 in a) & (1 not in a)  # 全为0
            flag4 = (1 in a) & (0 not in a)  # 全为1
            flag5 = (1 in a) & (0 in a)  # 0和1 都有

            # -----------------------------------------------------------------------------------------------#
            # 如果全为0（癌症），进入癌症文件夹
            if flag3:
                # 修改全0的分数 tempNEO_max
                print("修改前分数：", tempNEO_max)
                tempNEO_max = 0.3 * tempNEO_max + 0.7
                tempNEO_max = round(tempNEO_max, 2)
                print("修改后分数：", tempNEO_max)

                if int(top) < 0: top = 0
                if int(right) < 0: right = 0
                if int(left) < 0: left = 0
                if int(bottom) < 0: bottom = 0

                draw_new_scores(image, tempNEO_max, left, top, right, bottom)
                image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")), quality=95,
                           subsampling=0)
                return image,tempNEO_max

            # -----------------------------------------------------------------------------------------------#
            # 如果全为1（非癌症），进入这个非癌症文件夹
            if flag4:
                # 修改全1的分数 tempNONNEO_max
                print("修改前分数：", tempNONNEO_max)
                tempNONNEO_max = 0.3 - 0.3 * tempNONNEO_max
                tempNONNEO_max = round(tempNONNEO_max, 2)
                print("修改后分数：", tempNONNEO_max)

                if int(top) < 0: top = 0
                if int(right) < 0: right = 0
                if int(left) < 0: left = 0
                if int(bottom) < 0: bottom = 0

                draw_new_scores(image, tempNONNEO_max, left, top, right, bottom)
                image.save(os.path.join(all_save_path_allNONNEO, img_name.replace(".jpg", ".png")), quality=95,
                           subsampling=0)
                return image,tempNONNEO_max

            # -----------------------------------------------------------------------------------------------#
            # 如果同时有0和1，进入这个算法
            if flag5:
                if (class1 == 0):
                    # 修改分数 tempNEO_max
                    print("修改前分数：", tempNEO_max)
                    if tempNEO_max > 0.9:
                        if tempNEO_max - tempNONNEO_max < 0.1:
                            tempNEO_max = 0.3 * tempNEO_max + 0.7
                        else:
                            tempNEO_max = 0.2 * tempNEO_max + 0.5
                    if tempNEO_max < 0.9:
                        tempNEO_max = 0.5 * tempNEO_max + 0.5
                    tempNEO_max = round(tempNEO_max, 2)
                    print("修改后分数：", tempNEO_max)

                    if int(top) < 0: top = 0
                    if int(right) < 0: right = 0
                    if int(left) < 0: left = 0
                    if int(bottom) < 0: bottom = 0

                    draw_new_scores(image, tempNEO_max, left, top, right, bottom)
                    image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")), quality=95,
                               subsampling=0)
                    return image,tempNEO_max

                if (class1 == 1):
                    # 修改分数 tempNONNEO_max
                    print("修改前分数：", tempNONNEO_max)
                    if tempNONNEO_max > 0.9:
                        if tempNONNEO_max - tempNEO_max < 0.1:
                            tempNONNEO_max = 0.2 * tempNONNEO_max + 0.3
                        else:
                            tempNONNEO_max = 0.3 - 0.3 * tempNONNEO_max
                    if tempNONNEO_max < 0.9:
                        tempNONNEO_max = 0.5 - 0.5 * tempNONNEO_max
                    tempNONNEO_max = round(tempNONNEO_max, 2)
                    print("修改后分数：", tempNONNEO_max)

                    if int(top) < 0: top = 0
                    if int(right) < 0: right = 0
                    if int(left) < 0: left = 0
                    if int(bottom) < 0: bottom = 0

                    draw_new_scores(image, tempNONNEO_max, left, top, right, bottom)
                    image.save(os.path.join(all_save_path_allNONNEO, img_name.replace(".jpg", ".png")),
                               quality=95, subsampling=0)
                    return image,tempNONNEO_max

        # -----------------------------------------------------------------------------------------------#
        else:  # 没有识别出任何一个框
            # draw_new_scores(image,0, 0, 0, 0, 0)  # 这句也可以不要，因为没有生成结果，直接保存原图
            image.save(os.path.join(dir_save_path_fail_output, img_name.replace(".jpg", ".png")), quality=95,
                       subsampling=0)
            return image,0

        # ----------------------------------------------------------------------------------------------#
        confidence_down = confidence_down + 0.1
        confidence_up = confidence_down + 0.1

if __name__ == "__main__":
    image_path = '1.jpg'
    image = Image.open(image_path)
    predict11_single(image,image_path)
    print('success')