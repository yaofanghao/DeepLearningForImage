import numpy
import tensorflow as tf
from PIL import Image
from yolo_predict3 import YOLO
import os
from tqdm import tqdm
# from gen_xml import  GEN_Annotations # 6.21

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

if __name__ == "__main__":
    yolo = YOLO()
    # ----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'           表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'dir_predict'       表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    #   'heatmap'           表示进行预测结果的热力图可视化，详情查看下方注释。
    # ----------------------------------------------------------------------------------------------------------#
    mode = "predict"
    # -------------------------------------------------------------------------#
    #   crop                指定了是否在单张图片预测后对目标进行截取
    #   count               指定了是否进行目标的计数
    #   crop、count仅在mode='predict'时有效
    # -------------------------------------------------------------------------#
    crop = False
    count = False
    # -------------------------------------------------------------------------#
    #   dir_origin_path     指定了用于检测的图片的文件夹路径
    #   dir_save_path       指定了检测完图片的保存路径
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    # -------------------------------------------------------------------------#
    dir_origin_path = "img/"
    dir_save_path = "img_out"
    xml_save_path = "Annotations/"
    # -------------------------------------------------------------------------#
    #   heatmap_save_path   热力图的保存路径，默认保存在model_data下
    #   heatmap_save_path仅在mode='heatmap'有效
    # -------------------------------------------------------------------------#
    heatmap_save_path = "model_data/heatmap_vision.png"

    if mode == "predict":
        '''
        1、如果想要进行检测完的图片的保存，利用r_image.save("img.jpg")即可保存，直接在predict.py里进行修改即可。 
        2、如果想要获得预测框的坐标，可以进入yolo.detect_image函数，在绘图部分读取top，left，bottom，right这四个值。
        3、如果想要利用预测框截取下目标，可以进入yolo.detect_image函数，在绘图部分利用获取到的top，left，bottom，right这四个值
        在原图上利用矩阵的方式进行截取。
        4、如果想要在预测图上写额外的字，比如检测到的特定目标的数量，可以进入yolo.detect_image函数，在绘图部分对predicted_class进行判断，
        比如判断if predicted_class == 'car': 即可判断当前目标是否为车，然后记录数量即可。利用draw.text即可写字。
        '''
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                # r_image, out_scores, out_classes = yolo.detect_image(image, crop=crop, count=count)
                r_image, out_scores, out_classes, top, right, left, bottom = yolo.detect_image(image)
                r_image.show()

    elif mode == "dir_predict":
        # -----------------------------------#
        # !!! 唯一需要手动设置的地方：confidence_num
        confidence_num = 0.05
        confidence_down = confidence_num
        confidence_up = confidence_down + 0.1

        if confidence_down < 0.92:
            # 创建图片输出的文件夹
            dir_save_path_fail_output = "img_out_fail/"
            # 创建输出的文件夹：全0，全1，0和1都有
            all_save_path_allNEO = str(dir_save_path) + "_all_NEO/"
            all_save_path_allNONNEO = str(dir_save_path) + "_all_NONNEO/"

            if not os.path.exists(dir_save_path_fail_output):
                os.makedirs(dir_save_path_fail_output)
            if not os.path.exists(all_save_path_allNEO):
                os.makedirs(all_save_path_allNEO)
            if not os.path.exists(all_save_path_allNONNEO):
                os.makedirs(all_save_path_allNONNEO)
            if not os.path.exists(xml_save_path):
                os.makedirs(xml_save_path)

            # 统计识别和未识别图片个数
            fail = 0
            num_NEO_ture = 0
            num_NEO_flase = 0
            num_NONNEO_ture = 0
            num_NONNEO_flase = 0
            num_NEO_and_NONNEO = 0
            num_NEO_and_NONNEO_ture = 0
            num_NEO_and_NONNEO_flase = 0
            num1 = 0
            num2 = 0

            img_names = os.listdir(dir_origin_path)

            img_names.sort(key=lambda x:int(x.split('.')[0]))  # 按照1，2，3顺序读图片

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
                    r_image, out_scores, out_classes,top,right, left,bottom= yolo.detect_image(image)

                    # 分离名字 进行格式转换
                    filename, extension = os.path.splitext(img_name)
                    filename = int(filename)
                    # print(img_name)
                    # print(filename)
                # -----------------------------------------------------------------------------------------------#
                    out_scores_size = out_scores.numpy().size
                    # print('------------------')
                    # print(out_scores.numpy())
                    # print(out_scores.numpy().max()) # 这句不能有，会报错
                    # -----------------------------------------------------------------------------------------------------

                    ## 写文件  name class confidence top left right  bottom
                    f4 = open(os.path.join(os.getcwd(), 'result.txt'), 'a')
                    f4.write(str(img_name) + "\t")

                    if out_scores.numpy().size != 0:
                        f2 = open(os.path.join(os.getcwd(), str(confidence_num) + '_predict_report2.txt'), 'a')
                        f3 = open(os.path.join(os.getcwd(), str(confidence_num) + '_predict_report3.txt'), 'a')

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
                        tempNEO_max=round(tempNEO_max, 2)
                        tempNONNEO_max = numpy.max(tempNONNEO)
                        tempNONNEO_max = round(tempNONNEO_max, 2)
                        # print(tempNEO_max)
                        # print(tempNONNEO_max)

                        locat = out_scores.numpy().argmax(axis=None, out=None)  # 找最大值位置
                        # print(locat)
                        out_scores_max = out_scores.numpy().max()
                        out_scores_max =round(out_scores_max,2)   # 小数点后2位
                        # print("小数后两位")
                        # print(out_scores_max)
                        # print(type(out_scores.numpy()))
                        # print(out_classes.numpy())
                        a = out_classes.numpy()
                        class1 = a[locat]  # 最大值位置的类别
                        # print(class1)
                        # print(type(out_classes.numpy()))
                        # out_classes = out_classes.numpy().size
                        # print(out_classes.numpy())

                    # -----------------------------------------------------------------------------------------------#
                        # 判断语句
                        flag3 = (0 in a) & (1 not in a)  # 全为0
                        flag4 = (1 in a) & (0 not in a)  # 全为1
                        flag5 = (1 in a) & (0 in a)  # 0和1 都有

                    # -----------------------------------------------------------------------------------------------#
                        # 如果全为0（癌症），进入癌症文件夹
                        if flag3:
                            num1 += 1
                            if (filename < 500):
                               num_NEO_ture = num_NEO_ture + 1
                               print("正确的数量是：")
                               print(num_NEO_ture)
                            if (filename > 500):
                                num_NEO_flase = num_NEO_flase + 1
                                print("错误的数量是：")
                                print(num_NEO_flase)
                            r_image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

                            #修改全0的分数 tempNEO_max
                            print("修改前分数：", tempNEO_max)
                            tempNEO_max = 0.3*tempNEO_max + 0.7
                            tempNEO_max = round(tempNEO_max, 2)
                            print("修改后分数：", tempNEO_max)
                            out_scores_new = numpy.append(out_scores_new, tempNEO_max)

                            f2.write(img_name+"\t\t\t\t\t"+str(tempNEO_max))
                            f2.write('\r')
                            f2.close()

                    #-----------------------------------------------------------------------------------------------#
                        # 如果全为1（非癌症），进入这个非癌症文件夹
                        if flag4:
                            num2 += 1
                            if (filename > 500):
                                num_NONNEO_ture = num_NONNEO_ture + 1
                            if (filename < 500):
                                num_NONNEO_flase = num_NONNEO_flase + 1
                            r_image.save(os.path.join(all_save_path_allNONNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

                            #修改全1的分数 tempNONNEO_max
                            print("修改前分数：", tempNONNEO_max)
                            tempNONNEO_max = 0.3 - 0.3*tempNONNEO_max
                            tempNONNEO_max = round(tempNONNEO_max, 2)
                            print("修改后分数：", tempNONNEO_max)
                            out_scores_new = numpy.append(out_scores_new, tempNONNEO_max)

                    # -----------------------------------------------------------------------------------------------#
                        # 如果同时有0和1，进入这个算法
                        if flag5:
                            num_NEO_and_NONNEO += 1

                            if(class1 ==0 ):
                                 if (filename < 500):
                                      num1 += 1
                                      num_NEO_and_NONNEO_ture+=1
                                 else:
                                      num1 += 1
                                 r_image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),  quality=95, subsampling=0)

                                 # 修改分数 tempNEO_max
                                 print("修改前分数：", tempNEO_max)
                                 if tempNEO_max > 0.9:
                                     if tempNEO_max - tempNONNEO_max < 0.1:
                                         tempNEO_max = 0.3*tempNEO_max + 0.7
                                     else:
                                         tempNEO_max = 0.2 * tempNEO_max + 0.5
                                 if tempNEO_max < 0.9:
                                     tempNEO_max = 0.5*tempNEO_max + 0.5
                                 tempNEO_max=round(tempNEO_max, 2)
                                 print("修改后分数：", tempNEO_max)
                                 out_scores_new = numpy.append(out_scores_new, tempNEO_max)
                            if(class1 == 1 ):
                                if (filename > 500):
                                     num2+=1
                                     num_NEO_and_NONNEO_flase+=1
                                else:
                                    num2 += 1
                                r_image.save(os.path.join(all_save_path_allNONNEO,img_name.replace(".jpg", ".png")),   quality=95, subsampling=0)

                                # 修改分数 tempNONNEO_max
                                print("修改前分数：", tempNONNEO_max)
                                if tempNONNEO_max > 0.9:
                                    if tempNONNEO_max - tempNEO_max < 0.1:
                                        tempNONNEO_max = 0.2 * tempNONNEO_max + 0.3
                                    else:
                                        tempNONNEO_max = 0.3-0.3 * tempNONNEO_max
                                if tempNONNEO_max < 0.9:
                                    tempNONNEO_max = 0.5-0.5 * tempNONNEO_max
                                tempNONNEO_max = round(tempNONNEO_max, 2)
                                print("修改后分数：", tempNONNEO_max)
                                out_scores_new = numpy.append(out_scores_new, tempNONNEO_max)

                            f2.write(img_name+"\t\t\t\t\t"+str(tempNEO_max))
                            f2.write('\r')
                            f2.close()
                            f3.write(img_name+"\t\t\t\t\t"+str(tempNEO_max)+"\t\t\t\t\t"+str(tempNONNEO_max))
                            f3.write('\r')
                            f3.close()

                        # 预测结果存至result.txt
                        if int(top) < 0: top = 0
                        if int(right) < 0: right = 0
                        if int(left) < 0: left = 0
                        if int(bottom) < 0: bottom = 0
                        # print("top1是：")
                        # print(int(top))
                        # print("top1结束")
                        # print("right1是：")
                        # print(int(right))
                        # print("right1结束")
                        # print("left1是：")
                        # print(int(left))
                        # print("left1结束")
                        # print("bottom1是：")
                        # print(int(bottom))
                        # print("bottom1结束")
                        f4.write(str(class1) + "\t" +
                                 str(out_scores_max) + "\t" +
                                 str(int(top)) + "\t" +
                                 str(int(right)) + "\t" +
                                 str(int(left)) + "\t" +
                                 str(int(bottom)) + "\t")
                        f4.write('\r')
                        f4.close()

                        # 生成xml文件
                        # if class1 == 0:
                        #     anno = GEN_Annotations(img_name)
                        #     anno.set_size(image.width, image.height, 3)
                        #     anno.add_pic_attr("NEO", int(left), int(top), int(right), int(bottom))
                        #     anno.savefile(os.path.join(xml_save_path+str(filename)+'.xml'))
                        # if class1 == 1:
                        #     anno = GEN_Annotations(img_name)
                        #     anno.set_size(image.width, image.height, 3)
                        #     anno.add_pic_attr("NONEO", int(left), int(top), int(right), int(bottom))
                        #     anno.savefile(os.path.join(xml_save_path+str(filename)+'.xml'))

                    # -----------------------------------------------------------------------------------------------#
                    else: # 没有识别出任何一个框
                         r_image.save(os.path.join(dir_save_path_fail_output, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)
                         fail += 1
                         out_scores_new = numpy.append(out_scores_new, 0)

                         # 没有预测结果的存至result.txt,类别和坐标都记作0 图片名存至fail.txt
                         print("没有预测结果")
                         f4.write(str(0) + "\t" +
                                  str(0) + "\t" +
                                  str(0) + "\t" +
                                  str(0) + "\t" +
                                  str(0) + "\t" +
                                  str(0) + "\t")
                         f4.write('\r')
                         f_fail = open(os.path.join(os.getcwd(), 'fail.txt'), 'a')
                         f_fail.write(str('没有预测结果：') + "\t" + str(img_name))
                         f_fail.write('\r')
                         f_fail.close()

                         # 生成xml文件
                         # anno = GEN_Annotations(img_name)
                         # anno.set_size(image.width, image.height, 3)  # 图片尺寸
                         # anno.add_pic_attr("NEO", 0, 0, 0, 0)  # 设置name的类别,框的四个坐标值
                         # anno.savefile(os.path.join(xml_save_path + str(filename) + '.xml'))  # 导出xml

            # 修改后的分数写入txt
            f_new_scores = open(os.path.join(os.getcwd(), 'new_scores.txt'), 'a')
            for i in range(len(img_names)):
                f_new_scores.write(str(img_names[i])+'\t\t\t\t'+str(out_scores_new[i]))
                f_new_scores.write('\r')
            f_new_scores.close()

            # # -----------------------------------------------------------------------------------------------#
            # 打印出来结果
            print("全0癌症正确的数量是：")
            print(num_NEO_ture)

            print("全0癌症错误的数量是：")
            print(num_NEO_flase)

            print("全1非癌症正确的数量是：")
            print(num_NONNEO_ture)

            print("全1非癌症错误的数量是：")
            print(num_NONNEO_flase)

            print("未识别的数量是：")
            print(fail)

            print("混合的数量是：")
            print(num_NEO_and_NONNEO)

            print("未识别率：")
            print(fail / 538)

            print("错误识别率：")
            print((num_NEO_flase + num_NONNEO_flase) / 538)

            print("混合识别率：")
            print(num_NEO_and_NONNEO / 538)

            print("灵敏度：")
            print((num_NEO_ture + num_NEO_and_NONNEO_ture) / 334)

            print(num_NEO_ture)
            print(num_NEO_and_NONNEO_ture)

            print("特异度：")
            print((num_NONNEO_ture + num_NEO_and_NONNEO_flase) / 204)

            print("阳性预测值：")
            print((num_NEO_ture + num_NEO_and_NONNEO_ture) / num1)

            print("阴性预测值：")
            print((num_NONNEO_ture + num_NEO_and_NONNEO_flase) / num2)
            #----------------------------------------------------------------------------------------------#

            # 对应置信度的预测结果存至txt中
            ####   getcwd()  当前路径
            f = open(os.path.join(os.getcwd(), str(confidence_num) + '_predict_report.txt'), 'a')
            f.write("癌症正确的数量是:  " + str(num_NEO_ture))
            f.write("\r")
            f.write("癌症错误的数量是:  " + str(num_NEO_flase))
            f.write("\r")
            f.write("非癌症正确的数量是:  " + str(num_NONNEO_ture))
            f.write("\r")
            f.write("非癌症错误的数量是:  " + str(num_NONNEO_flase))
            f.write("\r")
            f.write("未识别的数量是:  " + str(fail))
            f.write("\r")
            f.write("混合的数量是:  " + str(num_NEO_and_NONNEO))
            f.write("\r")
            f.write("未识别率:  " + str((fail / 538) * 100) + '%')
            f.write("\r")
            f.write("错误识别率:  " + str(((num_NEO_flase + num_NONNEO_flase) / 538) * 100) + '%')
            f.write("\r")
            f.write("混合识别率:  " + str((num_NEO_and_NONNEO / 538) * 100) + '%')
            f.write("\r")
            f.write("灵敏度:  " + str(((num_NEO_ture + num_NEO_and_NONNEO_ture) / 334) * 100) + '%')
            f.write("\r")
            f.write("特异度:  " + str(((num_NONNEO_ture + num_NEO_and_NONNEO_flase) / 204) * 100) + '%')
            f.write("\r")
            f.write("阳性预测值:  " + str(((num_NEO_ture + num_NEO_and_NONNEO_ture) / num1) * 100) + '%')
            f.write("\r")
            f.write("阴性预测值:  " + str(((num_NONNEO_ture + num_NEO_and_NONNEO_flase) / num2) * 100) + '%')
            f.write("\r")
            f.close()

            confidence_down = confidence_down + 0.1
            confidence_up = confidence_down + 0.1
            #######################以上为修改部分##########################

    elif mode == "heatmap":
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                yolo.detect_heatmap(image, heatmap_save_path)

    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps' or 'dir_predict'.")
