import numpy
import tensorflow as tf
from PIL import Image
from yolo import YOLO
import os
from tqdm import tqdm

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

if __name__ == "__main__":
    yolo = YOLO()
    mode = "dir_predict"
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
    # -------------------------------------------------------------------------#
    #   heatmap_save_path   热力图的保存路径，默认保存在model_data下
    #   heatmap_save_path仅在mode='heatmap'有效
    # -------------------------------------------------------------------------#
    heatmap_save_path = "model_data/heatmap_vision.png"

    if mode == "dir_predict":
        # -----------------------------------#
        # !!! 唯一需要手动设置的地方：confidence_num
        confidence_num = 0.05
        confidence_down = confidence_num
        confidence_up = confidence_down + 0.1

        if confidence_down < 0.92:
            # 创建图片输出的文件夹
            dir_save_path_fail_output = "img_out_fail/"
            # 创建输出的文件夹：全0，全1，0和1都有
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
            # num_NEO_ture = 0
            # num_NEO_flase = 0
            # num_NONNEO_ture = 0
            # num_NONNEO_flase = 0
            # num_NEO_and_NONNEO = 0
            # num_NEO_and_NONNEO_ture = 0
            # num_NEO_and_NONNEO_flase = 0
            num1 = 0
            num2 = 0

            img_names = os.listdir(dir_origin_path)

            # img_names.sort(key=lambda x:int(x.split('.')[0]))  # 按照1，2，3顺序读图片

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
                    # filename = int(filename)
                    # print(img_name)
                    # print(filename)
                # -----------------------------------------------------------------------------------------------#
                    out_scores_size = out_scores.numpy().size
                    # print('------------------')
                    print(out_scores.numpy())
                    # print(out_scores.numpy().max()) # 这句不能有，会报错
                    # -----------------------------------------------------------------------------------------------------

                    ## 写文件  name class confidence top left right  bottom
                    # f4 = open(os.path.join(os.getcwd(), 'result.txt'), 'a')
                    # f4.write(str(img_name) + "\t")

                    if out_scores.numpy().size != 0:
                        # f2 = open(os.path.join(os.getcwd(), str(confidence_num) + '_predict_report2.txt'), 'a')
                        # f3 = open(os.path.join(os.getcwd(), str(confidence_num) + '_predict_report3.txt'), 'a')

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
                        tempNEO_max=round(tempNEO_max, 4)
                        tempNONNEO_max = numpy.max(tempNONNEO)
                        tempNONNEO_max = round(tempNONNEO_max, 4)
                        print(tempNEO_max)
                        print(tempNONNEO_max)

                        locat = out_scores.numpy().argmax(axis=None, out=None)  # 找最大值位置
                        # print(locat)
                        out_scores_max = out_scores.numpy().max()
                        out_scores_max =round(out_scores_max,4)   # 小数点后2位
                        # print("小数后两位")
                        # print(out_scores_max)
                        # print(type(out_scores.numpy()))
                        # print(out_classes.numpy())
                        a = out_classes.numpy()
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

                    # -----------------------------------------------------------------------------------------------#
                        # 如果全为0（癌症），进入癌症文件夹
                        if flag3:
                            num1 += 1
                            r_image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

                            #修改全0的分数 tempNEO_max
                            # print("修改前分数：", tempNEO_max)
                            # tempNEO_max = 0.3*tempNEO_max + 0.7
                            # tempNEO_max = round(tempNEO_max, 4)
                            # print("修改后分数：", tempNEO_max)
                            # out_scores_new = numpy.append(out_scores_new, tempNEO_max)
                            #
                            # f2.write(img_name+"\t\t\t\t\t"+str(tempNEO_max))
                            # f2.write('\r')
                            # f2.close()

                    #-----------------------------------------------------------------------------------------------#
                        # 如果全为1（非癌症），进入这个非癌症文件夹
                        if flag4:
                            num2 += 1
                            r_image.save(os.path.join(all_save_path_allNONNEO, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

                            #修改全1的分数 tempNONNEO_max
                            # print("修改前分数：", tempNONNEO_max)
                            # tempNONNEO_max = 0.3 - 0.3*tempNONNEO_max
                            # tempNONNEO_max = round(tempNONNEO_max, 4)
                            # print("修改后分数：", tempNONNEO_max)
                            # out_scores_new = numpy.append(out_scores_new, tempNONNEO_max)

                    # -----------------------------------------------------------------------------------------------#
                        # 如果同时有0和1，进入这个算法
                        if flag5:
                            # num_NEO_and_NONNEO += 1

                            if(class1 ==0 ):
                                r_image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),  quality=95, subsampling=0)
                                num1 += 1
                                 # 修改分数 tempNEO_max
                                 # print("修改前分数：", tempNEO_max)
                                 # if tempNEO_max > 0.9:
                                 #     if tempNEO_max - tempNONNEO_max < 0.1:
                                 #         tempNEO_max = 0.3*tempNEO_max + 0.7
                                 #     else:
                                 #         tempNEO_max = 0.2 * tempNEO_max + 0.5
                                 # if tempNEO_max < 0.9:
                                 #     tempNEO_max = 0.5*tempNEO_max + 0.5
                                 # tempNEO_max=round(tempNEO_max, 4)
                                 # print("修改后分数：", tempNEO_max)
                                 # out_scores_new = numpy.append(out_scores_new, tempNEO_max)

                            if(class1 == 1 ):
                                num2+=1
                                r_image.save(os.path.join(all_save_path_allNONNEO,img_name.replace(".jpg", ".png")),   quality=95, subsampling=0)

                                # 修改分数 tempNONNEO_max
                                # print("修改前分数：", tempNONNEO_max)
                                # if tempNONNEO_max > 0.9:
                                #     if tempNONNEO_max - tempNEO_max < 0.1:
                                #         tempNONNEO_max = 0.2 * tempNONNEO_max + 0.3
                                #     else:
                                #         tempNONNEO_max = 0.3-0.3 * tempNONNEO_max
                                # if tempNONNEO_max < 0.9:
                                #     tempNONNEO_max = 0.5-0.5 * tempNONNEO_max
                                # tempNONNEO_max = round(tempNONNEO_max, 4)
                                # print("修改后分数：", tempNONNEO_max)
                                # out_scores_new = numpy.append(out_scores_new, tempNONNEO_max)

                            # f2.write(img_name+"\t\t\t\t\t"+str(tempNEO_max))
                            # f2.write('\r')
                            # f2.close()
                            # f3.write(img_name+"\t\t\t\t\t"+str(tempNEO_max)+"\t\t\t\t\t"+str(tempNONNEO_max))
                            # f3.write('\r')
                            # f3.close()

                        # 预测结果存至result.txt
                        # if int(top) < 0: top = 0
                        # if int(right) < 0: right = 0
                        # if int(left) < 0: left = 0
                        # if int(bottom) < 0: bottom = 0
                        # # print("top1是：")
                        # # print(int(top))
                        # # print("top1结束")
                        # # print("right1是：")
                        # # print(int(right))
                        # # print("right1结束")
                        # # print("left1是：")
                        # # print(int(left))
                        # # print("left1结束")
                        # # print("bottom1是：")
                        # # print(int(bottom))
                        # # print("bottom1结束")
                        # f4.write(str(class1) + "\t" +
                        #          str(out_scores_max) + "\t" +
                        #          str(int(top)) + "\t" +
                        #          str(int(right)) + "\t" +
                        #          str(int(left)) + "\t" +
                        #          str(int(bottom)) + "\t")
                        # f4.write('\r')
                        # f4.close()

                    # -----------------------------------------------------------------------------------------------#
                    else: # 没有识别出任何一个框
                         r_image.save(os.path.join(dir_save_path_fail_output, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)
                         fail += 1
                         # out_scores_new = numpy.append(out_scores_new, 0)

                         # 没有预测结果的存至result.txt,类别和坐标都记作0 图片名存至fail.txt
                         # print("没有预测结果")
                         # f4.write(str(0) + "\t" +
                         #          str(0) + "\t" +
                         #          str(0) + "\t" +
                         #          str(0) + "\t" +
                         #          str(0) + "\t" +
                         #          str(0) + "\t")
                         # f4.write('\r')
                         # f_fail = open(os.path.join(os.getcwd(), 'fail.txt'), 'a')
                         # f_fail.write(str('没有预测结果：') + "\t" + str(img_name))
                         # f_fail.write('\r')
                         # f_fail.close()

            # 修改后的分数写入txt
            # f_new_scores = open(os.path.join(os.getcwd(), 'new_scores.txt'), 'a')
            # for i in range(len(img_names)):
            #     f_new_scores.write(str(img_names[i])+'\t\t\t\t'+str(out_scores_new[i]))
            #     f_new_scores.write('\r')
            # f_new_scores.close()

            # # -----------------------------------------------------------------------------------------------#
            # 打印出来结果
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

            # #----------------------------------------------------------------------------------------------#
            #
            # # 对应置信度的预测结果存至txt中
            # ####   getcwd()  当前路径
            # f = open(os.path.join(os.getcwd(), str(confidence_num) + '_predict_report.txt'), 'a')
            # f.write("癌症正确的数量是:  " + str(num_NEO_ture))
            # f.write("\r")
            # f.write("癌症错误的数量是:  " + str(num_NEO_flase))
            # f.write("\r")
            # f.write("非癌症正确的数量是:  " + str(num_NONNEO_ture))
            # f.write("\r")
            # f.write("非癌症错误的数量是:  " + str(num_NONNEO_flase))
            # f.write("\r")
            # f.write("未识别的数量是:  " + str(fail))
            # f.write("\r")
            # f.write("混合的数量是:  " + str(num_NEO_and_NONNEO))
            # f.write("\r")
            # f.write("未识别率:  " + str((fail / 538) * 100) + '%')
            # f.write("\r")
            # f.write("错误识别率:  " + str(((num_NEO_flase + num_NONNEO_flase) / 538) * 100) + '%')
            # f.write("\r")
            # f.write("混合识别率:  " + str((num_NEO_and_NONNEO / 538) * 100) + '%')
            # f.write("\r")
            # f.write("灵敏度:  " + str(((num_NEO_ture + num_NEO_and_NONNEO_ture) / 334) * 100) + '%')
            # f.write("\r")
            # f.write("特异度:  " + str(((num_NONNEO_ture + num_NEO_and_NONNEO_flase) / 204) * 100) + '%')
            # f.write("\r")
            # f.write("阳性预测值:  " + str(((num_NEO_ture + num_NEO_and_NONNEO_ture) / num1) * 100) + '%')
            # f.write("\r")
            # f.write("阴性预测值:  " + str(((num_NONNEO_ture + num_NEO_and_NONNEO_flase) / num2) * 100) + '%')
            # f.write("\r")
            # f.close()

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
