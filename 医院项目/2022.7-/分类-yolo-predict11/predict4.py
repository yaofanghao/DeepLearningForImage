import numpy
import tensorflow as tf
from PIL import Image
from yolo_predict2 import YOLO

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
    dir_save_path_fail = "img_out_fail"
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
                r_image, out_scores, out_classes = yolo.detect_image(image, crop=crop, count=count)
                r_image.show()

    elif mode == "dir_predict":
        import os
        from tqdm import tqdm

        ###########################以下为修改部分######################
        # 姚方浩 修改中
        # 2022.5.31 version1
        # 2022.6.6  version2-update
        # 2022.6.7  version3-update

        # debug调试用。请忽略有关logging的代码即可
        import logging

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.disable(logging.CRITICAL)  # 不显示debug日志记录。注释掉这一行可以看debug日志

        # -----------------------------------#
        # !!! 唯一需要手动设置的地方：confidence_num
        confidence_num = 0.1
        # -----------------------------------#
        confidence_down = confidence_num
        confidence_up = confidence_down + 0.1

        ########################## 修改部分  ################################################
        if confidence_down < 0.92:
            # 创建图片输出的文件夹
            # dir_save_path_NEO = str(confidence_down) + str('_') + str(confidence_up) + str('_') + str(
            #     dir_save_path) + "_NEO/"
            # dir_save_path_NONNEO = str(confidence_down) + str('_') + str(confidence_up) + str('_') + str(
            #     dir_save_path) + "_NONNEO/"
            dir_save_path_fail_output =  "img_out_fail/"

            # 创建输出的文件夹：全0，全1，0和1都有
            all_save_path_allNEO = str(dir_save_path) + "_all_NEO/"
            all_save_path_allNONNEO = str(dir_save_path) + "_all_NONNEO/"
            all_save_path_allNEOandNONNEO = str(dir_save_path) + "_all_NEO_and_NONNEO/"

            # if not os.path.exists(dir_save_path_NEO):
            #     os.makedirs(dir_save_path_NEO)
            # if not os.path.exists(dir_save_path_NONNEO):
            #     os.makedirs(dir_save_path_NONNEO)
            if not os.path.exists(dir_save_path_fail_output):
                os.makedirs(dir_save_path_fail_output)
            if not os.path.exists(all_save_path_allNEO):
                os.makedirs(all_save_path_allNEO)
            if not os.path.exists(all_save_path_allNONNEO):
                os.makedirs(all_save_path_allNONNEO)
            if not os.path.exists(all_save_path_allNEOandNONNEO):
                os.makedirs(all_save_path_allNEOandNONNEO)

            # 统计识别和未识别图片个数
            num_NEO = 0
            num_NONNEO = 0
            fail = 0

            img_names = os.listdir(dir_origin_path)
            ###tpdm  进度条
            for img_name in tqdm(img_names):
                ####如果图片末尾是  .....
                if img_name.lower().endswith(
                        ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                    image_path = os.path.join(dir_origin_path, img_name)
                    image = Image.open(image_path)

                    # 修改detect_image 的返回值
                    r_image, out_scores, out_classes = yolo.detect_image(image)

                    # 打印测试区域
                    # print('------------------')
                    # print(img_name)

                    logging.debug(out_scores)
                    out_scores_size = out_scores.numpy().size

                    print('------------------')
                    print(out_scores.numpy())
                    # print(out_scores.numpy().max()) # 这句不能有，会报错
                    # -----------------------------------------------------------------------------------------------------
                    # if out_scores.numpy().size == 0:
                    # -----------------------------------------------------------------------------------------------------
                    if out_scores.numpy().size != 0:

                        locat = out_scores.numpy().argmax(axis=None, out=None)  ##找最大值位置
                        print(locat)
                        # out_scores_max = out_scores.numpy().max()
                        # print(type(out_scores.numpy()))

                        print(out_classes.numpy())
                        a = out_classes.numpy()
                        class1 = a[locat]  ##找最大值位置 的类别
                        print(class1)
                        # print(type(out_classes.numpy()))
                        # out_classes = out_classes.numpy().size
                        # print(out_classes.numpy())

                        print('------------------')

                        ###化为张量
                        threshold = tf.constant([confidence_down])
                        threshold1 = tf.constant([confidence_up])
                        print(threshold)
                        # 比较 out_scores 和 threshold   结果 true or false

                        #flag = tf.greater(out_scores, threshold)

                        #flag1 = tf.greater(threshold1, out_scores)

                        #if any(flag & flag1):  # any()语法： 只要flag中存在True时即返回True
                            # flag2 = (predicted_class == 'NEO')
                        #flag2 = (0 in out_classes)  # 如果NEO（标签为0）在预测结果中，返回True
                        def judge():
                            for  i,j  in out_classes:
                               if(i^j==1):
                                  print("有0和1")
                                  return True

                        # if out_classes.any()==0 :

                        flag3 = (0 in a) & (1 not in a)  #全为0
                        flag4 = (1 in a) & (0 not in a)  #全为1
                        flag5 = (1 in a) & (0 in a)  #0和1 都有
                        if flag3:  # 如果全为0（癌症），进入癌症文件夹
                            flag2 = 1
                            print(flag2)
                            r_image.save(os.path.join(all_save_path_allNEO, img_name.replace(".jpg", ".png")),
                                                         quality=95, subsampling=0)
                        if flag4:  # 如果全为1（非癌症），进入这个非癌症文件夹
                            flag2 = 2
                            print(flag2)
                            r_image.save(os.path.join(all_save_path_allNONNEO, img_name.replace(".jpg", ".png")),
                                                         quality=95, subsampling=0)
                        if flag5:  # 如果同时有0和1，进入这个算法
                            flag2 = 3
                            print(flag3)
                            r_image.save(os.path.join(all_save_path_allNEOandNONNEO, img_name.replace(".jpg", ".png")),
                                         quality=95, subsampling=0)
                        # if (judge()):
                        #     flag2 = 3
                        #     print(flag2)

                    #     if flag2:
                    #             r_image.save(os.path.join(dir_save_path_NEO, img_name.replace(".jpg", ".png")),
                    #                              quality=95, subsampling=0)
                    #             num_NEO += 1
                    #         else:
                    #             r_image.save(os.path.join(dir_save_path_NONNEO, img_name.replace(".jpg", ".png")),
                    #                              quality=95, subsampling=0)
                    #             num_NONNEO += 1
                    else:
                         r_image.save(os.path.join(dir_save_path_fail_output, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)
                         fail += 1

            # 修改中---预测结果保存至txt中0
            total = num_NEO + num_NONNEO + fail
            accuracy = num_NEO / total
            ####   getcwd()  当前路径
            # f = open(os.path.join(os.getcwd(), str(confidence_down) + str('_') + str(confidence_up) + '_predict.txt'),
            #          'a')
            # f.write("预测的图片总数:  " + str(total))
            # f.write("\r")
            # f.write("---识别出置信框:  " + str(num_NEO + num_NONNEO))
            # f.write("\r")
            # f.write(" |---识别为肿瘤性:  " + str(num_NEO))
            # f.write("\r")
            # f.write(" |---识别为非肿瘤:  " + str(num_NONNEO))
            # f.write("\r")
            # f.write("---未识别出置信框:  " + str(fail))
            # f.write("\r")
            # f.write("识别肿瘤性的比例:  " + str(accuracy * 100) + "%")
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
