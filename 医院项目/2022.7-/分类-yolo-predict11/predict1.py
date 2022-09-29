import tensorflow as tf
from PIL import Image
from yolo_predict1 import YOLO

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
    dir_save_path = "img_out/"
    dir_save_path_fail = "img_out_fail/"
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
                r_image = yolo.detect_image(image, crop=crop, count=count)
                r_image.show()

    elif mode == "dir_predict":
        import os
        from tqdm import tqdm

        ##############################################################
        # 姚方浩 修改中
        # 2022.5.31 version1
        # 2022.6.6  version2-update
        import logging

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.disable(logging.CRITICAL)

        ##################################
        # !!!唯一需要手动设置的地方：confidence_num
        confidence_num = 0.1
        #################################

        img_names = os.listdir(dir_origin_path)

        dir_save_path_conf = str(confidence_num) + str('_') + "img_out/"
        dir_save_path_fail_conf = str(confidence_num) + str('_') + "img_out_fail/"
        if not os.path.exists(dir_save_path_conf):
            os.makedirs(dir_save_path_conf)
        if not os.path.exists(dir_save_path_fail_conf):
            os.makedirs(dir_save_path_fail_conf)

        # 统计识别和未识别图片个数
        success = 0
        success_multi = 0  # 识别出多个框
        fail = 0

        for img_name in tqdm(img_names):
            if img_name.lower().endswith(
                    ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path = os.path.join(dir_origin_path, img_name)
                image = Image.open(image_path)
                r_image, out_scores = yolo.detect_image(image)

                # 展示预测结果：图片名、预测的置信度
                print(img_name)
                # out_scores=out_scores.numpy()
                # out_scores=tf.as_string(out_scores)
                logging.debug(out_scores)
                # logging.debug(tf.shape(out_scores))
                out_scores_size = out_scores.numpy().size
                logging.debug(out_scores_size)

                threshold = tf.constant([confidence_num])
                # threshold = tf.constant([confidence_num],shape=(1,out_scores_size))
                # if out_scores_size == 0 or out_scores_size == 1:
                #     threshold = tf.constant([confidence_num])
                # else:
                #     threshold = tf.constant([confidence_num, confidence_num])
                #     success_multi += 1
                if out_scores_size > 1:
                    success_multi += 1
                else:
                    pass

                # 比较 out_scores 和 threshold
                # if predict result  > confidence 预测图片保存至 置信度+_img_out
                # if predict result <= confidence 预测图片保存至 置信度+_img_out_fail
                flag = tf.greater(out_scores, threshold)
                if any(flag):  # any()语法： 只要flag中存在True时即返回True
                    r_image.save(os.path.join(dir_save_path_conf, img_name.replace(".jpg", ".png")), quality=95,
                                 subsampling=0)
                    success += 1
                else:
                    r_image.save(os.path.join(dir_save_path_fail_conf, img_name.replace(".jpg", ".png")), quality=95,
                                 subsampling=0)
                    fail += 1

        success_ratio = success / (success + fail)
        print("识别到置信框的图片数:" + str(success))
        print("---(其中，识别到多个置信框的图片数:)" + str(success_multi))
        print("未识别到置信框的图片数:" + str(fail))
        print("识别比例:" + str(success_ratio * 100) + "%")
        ##############################################################

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