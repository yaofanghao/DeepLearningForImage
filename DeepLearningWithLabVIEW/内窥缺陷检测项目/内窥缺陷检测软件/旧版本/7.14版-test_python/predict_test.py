"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/7/10 11:27
    @Filename: predict_test.py
    @Software: PyCharm     
"""

# 用于制作exe的py文件 可供labview调用
# 具体参数配置在 argparse.txt 中设置

# -*- coding: utf-8 -*-
import os
import sys

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
from tqdm import tqdm
import colorsys
import copy
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image, ImageFont, ImageDraw
from nets.hrnet import HRnet
from utils.utils import cvtColor, preprocess_input, resize_image, show_config

# 数据库读写模块
import pyodbc
from datetime import datetime

# 日志调试模块
import logging
# logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# 计时模块
import datetime as dt


# #########################参数设置区域
_classes_txt = "class_name.txt"  # 分类标签文件
_classes_gbk_txt = "class_name_gbk.txt"  # 分类标签文件中文版
argparse_txt = "argparse.txt"  # 配置参数文件
current_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(current_dir, 'predict_result.mdb')  # 构造数据库文件，并连接到Access数据库，DBQ需要是绝对路径

# import argparse, sys
# parser = argparse.ArgumentParser(description='Test for argparse')
# parser.add_argument('--mode', '-m', type=int,
#                     help='mode 0或1 0为单张图片预测 1为视频预测 默认为1',
#                     default=1)   # required=True,
# parser.add_argument('--use_gpu', '-u', type=int,
#                     help='use_gpu 是否使用GPU环境 默认为1',
#                     default=1)
# parser.add_argument('--timeF', '-t', type=int,
#                     help='timeF 视频帧计数间隔频率 默认为10',
#                     default=10)
# args = parser.parse_args()


def load_arg():
    # 方法一 2023.4.26 以argparse方式载入参数
    # try:
    #     logging.info("mode:{} \t use_gpu:{} \t timeF:{} ".format(args.mode, args.use_gpu, args.timeF))
    # except Exception as e:
    #     print(e)
    # return args.mode, args.use_gpu, args.timeF

    # 方法二 以读取配置文件argparse.txt的方式载入参数
    # 配置参数说明：
    # 第一项为预测模式 0或1 0为单张图片预测 1为视频预测 默认为1
    # 第二项为是否使用gpu环境 True或False
    # 第三项为视频帧计数间隔频率 影响视频检测速率，可任意设置，建议值10-30之间
    # 第四项为待检测图片\视频的相对路径

    f_arg = open(argparse_txt, "r", encoding='gbk')
    lines_arg = f_arg.read().splitlines()
    logging.info("success load arg from: {}".format(argparse_txt))
    logging.info("setting mode: {} \t use_gpu:{} \t timeF:{} "
                 .format(lines_arg[0], lines_arg[1], lines_arg[2]))
    logging.info("success read filename: {} \t".format(lines_arg[3]))
    return lines_arg[0], lines_arg[1], lines_arg[2], lines_arg[3]


def gpu_enable(_use_gpu=None):

    current_time = dt.datetime.now()
    print("Current time 0:", current_time.strftime("%Y-%m-%d %H:%M:%S"))

    if _use_gpu:  # 使用GPU
        logging.info("use gpu")
        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        # 设置可见的GPU设备
        # physical_devices = tf.config.list_physical_devices('GPU')
        # tf.config.experimental.set_visible_devices(physical_devices[0], 'GPU')
        #
        # # 在必要时分配显存
        # for device in physical_devices:
        #     tf.config.experimental.set_memory_growth(device, True)


    else:  # 使用CPU
        logging.info("use cpu")
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def read_txt_lines(_classes_txt=None, _classes_gbk_txt=None):
    __name_classes = []
    __name_classes_gbk = []
    f = open(_classes_txt, "r")
    f_gbk = open(_classes_gbk_txt, "r", encoding='utf-8')
    lines = f.read().splitlines()
    lines_gbk = f_gbk.read().splitlines()
    for i in range(len(lines)):
        __name_classes.append(lines[i])
        __name_classes_gbk.append(lines_gbk[i])
    return __name_classes, __name_classes_gbk


# 检测表名是否已存在的函数
def table_exists(table_name, db_file_path):
    conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_file_path
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # 获取数据库中的所有表
    tables = cursor.tables(tableType='TABLE')

    # 遍历表列表，判断特定表是否存在
    for table in tables:
        if table.table_name == table_name:
            cursor.close()
            conn.close()
            return True

    cursor.close()
    conn.close()
    return False


class HRNetSegmentation(object):

    def __init__(self, **kwargs):
        self.model_path = 'C:\\Users\\Rainy\\Desktop\\test_python\\logs.h5'
        self.num_classes = 9  # 所需要区分的类的个数+1
        self.backbone = "hrnetv2_w32"  # 主干特征提取网络 hrnetv2_w18 hrnetv2_w32 hrnetv2_w48
        self.input_shape = [480, 480]  # 输入模型的图片尺寸
        self.colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                       (0, 128, 128), (128, 128, 128), (64, 0, 0)]

        #   加载模型
        self.model = HRnet([self.input_shape[0], self.input_shape[1], 3], self.num_classes, backbone=self.backbone)
        self.model.load_weights(self.model_path)
        logging.info('success load model: {}'.format(self.model_path))

    @tf.function
    def get_pred(self, photo):
        preds = self.model(photo, training=False)
        return preds

    #   检测图片
    def detect_image(self, image=None, name_classes=None, name_classes_gbk=None,
                     file_name = None, img_name=None, dir_save_path=None, result_txt=None):
        image = cvtColor(image)
        #   对输入图像进行一个备份，后面用于绘图
        old_img = copy.deepcopy(image)
        orininal_h = np.array(image).shape[0]
        orininal_w = np.array(image).shape[1]
        #   给图像增加灰条，实现不失真的resize
        image_data, nw, nh = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        #   归一化+添加上batch_size维度
        image_data = np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0)

        #   图片传入网络进行预测
        pr = self.get_pred(image_data)[0].numpy()
        #   将灰条部分截取掉
        pr = pr[int((self.input_shape[0] - nh) // 2): int((self.input_shape[0] - nh) // 2 + nh),
             int((self.input_shape[1] - nw) // 2): int((self.input_shape[1] - nw) // 2 + nw)]
        #   进行图片的resize
        pr = cv2.resize(pr, (orininal_w, orininal_h), interpolation=cv2.INTER_LINEAR)
        #   取出每一个像素点的种类
        pr = pr.argmax(axis=-1)

        seg_img = np.reshape(np.array(self.colors, np.uint8)[np.reshape(pr, [-1])], [orininal_h, orininal_w, -1])
        image = Image.fromarray(np.uint8(seg_img))
        image = Image.blend(old_img, image, 0.5)

        # 修改显示字体格式
        font = ImageFont.truetype(font='model_data/simhei.ttf',
                                  size=np.floor(3e-2 * image.size[1] + 15).astype('int32'))  # 修改字体大小
        draw = ImageDraw.Draw(image)
        classes_nums = np.zeros([self.num_classes])
        output_class_name = np.array([], dtype=int)  # 存放预测类别结果的数组
        step = 1  # 在图上绘制预测类别的显示间隔
        for i in range(self.num_classes):
            num = np.sum(pr == i)
            draw.text((30, 30 * 0), str("【预测结果】"), fill='red', font=font)
            if (num > 0) & (name_classes is not None) & (i > 0):
                # draw.text((50 * i, 50 * i), str(name_classes_gbk[i]), fill='red', font=font)
                draw.text((70, 30 * step), str(name_classes_gbk[i]), fill='red', font=font)
                step = step + 1
                output_class_name = np.append(output_class_name, i)
            classes_nums[i] = num

        #  这张图要有检测结果才进入该循环
        if output_class_name.size > 0:
            max_output_class_name = np.max(output_class_name)

            # 2023.3.3 只保存有预测结果的图片（只有background不算作有预测结果）
            # 代码原理：最大预测结果类别大于0，说明预测出的不是只有background，此时保存图片
            if max_output_class_name > 0:
                logging.info("\n")
                logging.info("{}-发现缺陷--{}".format(img_name, output_class_name))
                # 存放预测结果的文件夹
                result_txt.write(img_name)
                result_txt.write("\r")
                result_txt.write("  识别出的种类有： ")

                # 2023.6.29 【新要求】补充 ----------数据库读写模块
                # 插入数据库中检测结果的字符串
                insert_detect_result = ""

                # 连接数据库
                conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(db_file_path)
                logging.info("成功创建并打开数据库，路径为{}".format(db_file_path))
                # logging.info(conn_str)
                conn = pyodbc.connect(conn_str)
                # 创建游标
                cursor = conn.cursor()

                # 如果不存在名为file_name的表，则创建新表
                # 因为数据库表名通常不支持点号，所以将.替换为_
                if not table_exists(table_name=file_name.replace(".", "_"), db_file_path=db_file_path):
                    create_table_sql = '''
                        CREATE TABLE {} (
                            时间 DATETIME,
                            图片名 VARCHAR(50),
                            检测结果 VARCHAR(50)
                        )
                    '''.format(file_name.replace(".", "_"))
                    cursor.execute(create_table_sql)
                    logging.info("创建完成！")
                if table_exists(table_name=file_name.replace(".", "_"), db_file_path=db_file_path):
                    logging.info("已有表！")


                for i in range(output_class_name.shape[0]):
                    if (output_class_name[i] > 0) :
                        temp = output_class_name[i]
                        logging.info("识别出：{}--{}".format(temp, name_classes_gbk[temp]))
                        result_txt.write("    " + str(name_classes_gbk[temp]) + "\t")
                        insert_detect_result = insert_detect_result + " " + str(name_classes_gbk[temp])

                    # 已废弃代码 不用：
                    # # 2023.6.29 【新要求】如果识别预测结果为白班，则视为多余物
                    # # 白班是class_name.txt中的第7项
                    # if (output_class_name[i] > 0) & (output_class_name[i] == 7):
                    #     temp = 1  # 多余物是class_name.txt中的第1项（从0开始计数）
                    #     logging.info("识别出：{}--{}".format(temp, name_classes_gbk[temp]))
                    #     result_txt.write("    " + str(name_classes_gbk[temp]) + "\t")
                    #     insert_detect_result = insert_detect_result + " " + str(name_classes_gbk[temp])

                    # 2023.6.3 补充焊接缺陷的判定
                    if output_class_name[i] == 8:  # 标签中对应第10号是是焊接缺陷
                        result_txt.write("\n  识别出焊接缺陷！程序立即停止！")
                        image.save(os.path.join(dir_save_path, img_name))
                        insert_detect_result = insert_detect_result + " " + str(name_classes_gbk[10])

                        # 焊接缺陷写入数据库的代码单独列出：
                        insert_data_sql = '''
                            INSERT INTO {} VALUES (?, ?, ?)
                        '''.format(file_name.replace(".", "_"))
                        values = (datetime.now(), img_name, insert_detect_result)
                        cursor.execute(insert_data_sql, values)
                        conn.commit()
                        cursor.close()
                        conn.close()
                        logging.info("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的表 [{}] 中！"
                                     .format(img_name, insert_detect_result, file_name.replace(".", "_")))
                        logging.error("识别出焊接缺陷！程序立即停止！")
                        sys.exit(1)  # 异常退出，程序立即终止

                # 已废弃代码 不用：
                # # 2023.6.29 【新要求】如果识别预测结果为白班，则视为多余物
                # # 白班是class_name.txt中的第7项
                # if max_output_class_name == 7:
                #     max_output_class_name = 1

                result_txt.write("\r")
                result_txt.write("  预测概率值最高的类别为： " + name_classes_gbk[max_output_class_name])

                # 2023.6.29 【新要求】插入数据到数据库表中
                # 格式示例： 时间 图片名 检测结果
                insert_data_sql = '''
                    INSERT INTO {} VALUES (?, ?, ?)
                '''.format(file_name.replace(".", "_"))
                values = (datetime.now(), img_name, insert_detect_result)
                cursor.execute(insert_data_sql, values)

                conn.commit()
                # 关闭连接
                cursor.close()
                conn.close()
                logging.info("成功写入数据 [名称:{}] [检测结果:{}] 到数据库的表 [{}] 中！"
                             .format(img_name, insert_detect_result, file_name.replace(".", "_")))
                # logging.info("写入数据库模块结束！")

            result_txt.write("\r")
            image.save(os.path.join(dir_save_path, img_name))

    def detect_image_no_access(self, image=None, name_classes=None, name_classes_gbk=None,
                     img_name=None, dir_save_path=None):
        image = cvtColor(image)
        #   对输入图像进行一个备份，后面用于绘图
        old_img = copy.deepcopy(image)
        orininal_h = np.array(image).shape[0]
        orininal_w = np.array(image).shape[1]
        #   给图像增加灰条，实现不失真的resize
        image_data, nw, nh = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        #   归一化+添加上batch_size维度
        image_data = np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0)

        #   图片传入网络进行预测
        pr = self.get_pred(image_data)[0].numpy()
        #   将灰条部分截取掉
        pr = pr[int((self.input_shape[0] - nh) // 2): int((self.input_shape[0] - nh) // 2 + nh),
             int((self.input_shape[1] - nw) // 2): int((self.input_shape[1] - nw) // 2 + nw)]
        #   进行图片的resize
        pr = cv2.resize(pr, (orininal_w, orininal_h), interpolation=cv2.INTER_LINEAR)
        #   取出每一个像素点的种类
        pr = pr.argmax(axis=-1)

        seg_img = np.reshape(np.array(self.colors, np.uint8)[np.reshape(pr, [-1])], [orininal_h, orininal_w, -1])
        image = Image.fromarray(np.uint8(seg_img))
        image = Image.blend(old_img, image, 0.7)

        # 修改显示字体格式
        font = ImageFont.truetype(font='model_data/simhei.ttf',
                                  size=np.floor(3e-2 * image.size[1] + 15).astype('int32'))  # 修改字体大小
        draw = ImageDraw.Draw(image)
        classes_nums = np.zeros([self.num_classes])
        output_class_name = np.array([], dtype=int)  # 存放预测类别结果的数组
        step = 1  # 在图上绘制预测类别的显示间隔
        for i in range(self.num_classes):
            num = np.sum(pr == i)
            draw.text((30, 30 * 0), str("【预测结果】"), fill='red', font=font)
            if (num > 0) & (name_classes is not None) & (i > 0):
                # draw.text((50 * i, 50 * i), str(name_classes_gbk[i]), fill='red', font=font)
                draw.text((70, 30 * step), str(name_classes_gbk[i]), fill='red', font=font)
                step = step + 1
                output_class_name = np.append(output_class_name, i)
            classes_nums[i] = num

        #  这张图要有检测结果才进入该循环
        if output_class_name.size > 0:
            max_output_class_name = np.max(output_class_name)

            # 2023.3.3 只保存有预测结果的图片（只有background不算作有预测结果）
            # 代码原理：最大预测结果类别大于0，说明预测出的不是只有background，此时保存图片
            if max_output_class_name > 0:
                logging.info("{}-发现缺陷--{}".format(img_name, output_class_name))

                for i in range(output_class_name.shape[0]):
                    if (output_class_name[i] > 0) :
                        temp = output_class_name[i]
                        logging.info("识别出：{}--{}".format(temp, name_classes_gbk[temp]))

                    # 2023.6.3 补充焊接缺陷的判定
                    if output_class_name[i] == 8:  # 标签中对应第10号是是焊接缺陷
                        image.save(os.path.join(dir_save_path, img_name))

                        logging.error("识别出焊接缺陷！程序立即停止！")
                        sys.exit(1)  # 异常退出，程序立即终止

            image.save(os.path.join(dir_save_path, img_name))


def predict_main(mode=None, name_classes=None, name_classes_gbk=None, timeF=None, filename=None):

    current_time = dt.datetime.now()
    print("Current time 1:", current_time.strftime("%Y-%m-%d %H:%M:%S"))

    hrnet = HRNetSegmentation()
    if mode == 0:
        image = Image.open(str(filename))
        try:
            logging.info('success read image: ' + str(filename))
            file_rootname, _ = os.path.splitext(filename)
        except Exception as e:
            raise Exception(e)
        dir_save_path = str(file_rootname) + "_img_out/"
        if not os.path.exists(dir_save_path):
            os.makedirs(dir_save_path)
        f1 = open(os.path.join(dir_save_path, str(file_rootname) + '_predict_result.txt'), 'w', encoding='gbk')

        logging.info("start image predict")
        hrnet.detect_image(image=image, name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                           file_name=filename, img_name=filename, dir_save_path=dir_save_path, result_txt=f1)
        f1.close()
        logging.info("success, predict done!")
        logging.info("\n")

    if mode == 1:
        # video_name = input("Input video filename:")
        try:
            logging.info('success read video ' + str(filename))
            file_rootname, _ = os.path.splitext(filename)
        except Exception as e:
            raise Exception(e)
        output_dir = str(file_rootname) + '_img/'  # 保存图片文件夹路径
        output_img_type = '.jpg'  # 保存图片的格式
        vc = cv2.VideoCapture(filename)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if vc.isOpened():
            rval, frame = vc.read()
        else:
            raise Exception('Video do not exist.')
        c = 1  # 统计帧数
        while rval:  # 循环读取视频帧
            rval, frame = vc.read()
            if not rval:
                break
            if c % int(timeF) == 0:  # 每隔timeF帧进行存储
                cv2.imwrite(output_dir + str(c) + output_img_type, frame)
                logging.info('success read frame No.' + str(c))
            c = c + 1
            cv2.waitKey(1)
        vc.release()
        # ------------------对img_out文件中图片批量预测
        logging.info("start video predict")
        dir_save_path = str(file_rootname) + "_img_out/"
        if not os.path.exists(dir_save_path):
            os.makedirs(dir_save_path)
        img_names = os.listdir(output_dir)
        img_names.sort(key=lambda x: int(x.split('.')[0]))  # 按照1，2，3 顺序读图片
        f1 = open(os.path.join(dir_save_path, str(file_rootname) + '_predict_result.txt'), 'a', encoding='gbk')
        for img_name in tqdm(img_names):
            image_path = os.path.join(output_dir, img_name)
            image = Image.open(image_path)
            # 预测图片，只保存有预测结果图片
            hrnet.detect_image(image, name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                               file_name = filename, img_name=img_name, dir_save_path=dir_save_path, result_txt=f1)
        f1.close()
        logging.info("success, all predict done!")

    # 2023.7.7 连续运行，输入图片预测
    if mode == 2:
        while True:
            img = input('Input image filename:')
            if img == "q":
                sys.exit(1)  # 程序退出

            try:
                image = Image.open(str(img))
                print('success read image:{} '.format(str(img)))
                file_rootname, _ = os.path.splitext(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                dir_save_path = str(file_rootname) + "_img_out/"
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                f1 = open(os.path.join(dir_save_path, str(file_rootname) + '_predict_result.txt'), 'w',
                          encoding='gbk')

                current_time = dt.datetime.now()
                print("Current time 3:", current_time.strftime("%Y-%m-%d %H:%M:%S"))

                logging.info("start image predict")
                hrnet.detect_image(image=image, name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                                   file_name=img, img_name=img, dir_save_path=dir_save_path,
                                   result_txt=f1)

                current_time = dt.datetime.now()
                print("Current time 4:", current_time.strftime("%Y-%m-%d %H:%M:%S"))

                f1.close()
                logging.info("success, predict done!")


def func():
    _mode, _use_gpu, _timeF, _filename = load_arg()

    # gpu or cpu 方式加载程序
    gpu_enable(_use_gpu=int(_use_gpu))

    # 读取标签文件
    _name_classes, _name_classes_gbk = read_txt_lines(_classes_txt=_classes_txt,
                                                      _classes_gbk_txt=_classes_gbk_txt)

    # 进入预测 单张图片/视频
    predict_main(mode=int(_mode), name_classes=_name_classes, name_classes_gbk=_name_classes_gbk,
                 timeF=_timeF, filename=_filename)

    return 1


def func_test(_mode, _use_gpu, _timeF, _filename):

    # gpu or cpu 方式加载程序
    gpu_enable(_use_gpu=int(_use_gpu))

    # 读取标签文件
    _name_classes, _name_classes_gbk = read_txt_lines(_classes_txt=_classes_txt,
                                                      _classes_gbk_txt=_classes_gbk_txt)

    # 进入预测 单张图片/视频
    predict_main(mode=int(_mode), name_classes=_name_classes, name_classes_gbk=_name_classes_gbk,
                 timeF=_timeF, filename=_filename)

    return 1


# func_test(2,0,10,"1.jpg")

# # 方法1 2023.7.13-ok 目前在labview中测试，可以调用句柄hrnet_model实现只调用一次模型
# https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000xCdrCAE&l
def ObjInitialize(_use_gpu=0):
    # gpu or cpu 方式加载程序
    gpu_enable(_use_gpu=int(_use_gpu))

    hrnet = HRNetSegmentation()
    hrnet.model = HRnet([480, 480, 3], hrnet.num_classes, backbone=hrnet.backbone)
    hrnet.model.load_weights(hrnet.model_path)
    return hrnet

def predict(img, hrnet):
    # 读取标签文件
    name_classes, name_classes_gbk = read_txt_lines(_classes_txt=_classes_txt,
                                                      _classes_gbk_txt=_classes_gbk_txt)

    # 进入预测 单张图片/视频
    while True:
        # img = input('Input image filename:')
        if img == "q":
            sys.exit(1)  # 程序退出

        try:
            image = Image.open(str(img))
            print('success read image:{} '.format(str(img)))
            file_rootname, _ = os.path.splitext(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            dir_save_path = str(file_rootname) + "_img_out/"
            if not os.path.exists(dir_save_path):
                os.makedirs(dir_save_path)
            f1 = open(os.path.join(dir_save_path, str(file_rootname) + '_predict_result.txt'), 'w',
                      encoding='gbk')

            logging.info("start image predict")
            # hrnet.detect_image(image=image, name_classes=name_classes, name_classes_gbk=name_classes_gbk,
            #                 file_name=img, img_name=img, dir_save_path=dir_save_path,
            #                 result_txt=f1)

            hrnet.detect_image_no_access(image=image, name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                                         img_name=img, dir_save_path=dir_save_path)

            f1.close()
            logging.info("success, predict done!")
        return 1

# hrnet_model = ObjInitialize(0)
# predict(img="1.jpg", hrnet=hrnet_model)
# predict(img="2.jpg", hrnet=hrnet_model)
# predict(img="3.jpg", hrnet=hrnet_model)
# predict(img="4.jpg", hrnet=hrnet_model)


# # 方法2
# hrnet_model = ObjInitialize(0)
# while True:
#     img = input('Input image filename:')
#     predict(img=img, hrnet=hrnet_model)


# 2023.7.12 晚 测试
# def test(i, model):
#     if i==0:
#         hrnet_model = ObjInitialize(0)
#         model = hrnet_model
#         return model
#     if i>=0:
#         img = input('Input image filename:')
#         predict(img=img, hrnet=model)
#         return 1
#
# def test_out():
#     i = 0
#     model = None
#     while True:
#         print("i= ", i)
#         if i==0:
#             model = test(i, model=None)
#             i = i+1
#         if i>=0:
#             test(i, model=model)

# global model   # 模型作为全局变量
# test_out()


