"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/4/25 11:07
    @Filename: predict_for_exe.py
    @Software: PyCharm     
"""
# 用于制作exe的py文件 可供labview调用

# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
from tqdm import tqdm
import colorsys
import copy
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image, ImageFont, ImageDraw
from nets.hrnet import HRnet
from utils.utils import cvtColor, preprocess_input, resize_image, show_config

# 日志调试模块
import logging
# logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)


# #########################参数设置区域
_classes_txt = "class_name.txt"  # 分类标签文件
_classes_gbk_txt = "class_name_gbk.txt"  # 分类标签文件中文版
argparse_txt = "argparse.txt"  # 配置参数文件
# import argparse, sys
# parser = argparse.ArgumentParser(description='Test for argparse')
# parser.add_argument('--mode', '-m', type=int,
#                     help='mode 0或1 0为单张图片预测 1为视频预测 默认为1',
#                     default=1)   # required=True,
# parser.add_argument('--use_gpu', '-u', type=bool,
#                     help='use_gpu 是否使用GPU环境 默认为True',
#                     default=True)
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
    f_arg = open(argparse_txt, "r", encoding='utf-8')
    lines_arg = f_arg.read().splitlines()
    logging.info("success load arg from:{}".format(argparse_txt))
    logging.info("mode:{} \t use_gpu:{} \t timeF:{} ".format(lines_arg[4], lines_arg[5], lines_arg[6]))
    return lines_arg[4], lines_arg[5], lines_arg[6]


def gpu_enable(_use_gpu=None):
    if _use_gpu:  # 使用GPU
        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    else:  # 使用CPU
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


class HRNetSegmentation(object):
    # _defaults = {
    #     "model_path": 'logs/best_epoch_weights.h5',  # 模型权重
    #     "num_classes": 10,  # 所需要区分的类的个数+1
    #     # ----------------------------------------#
    #     #   所使用的的主干网络：
    #     #   hrnetv2_w18
    #     #   hrnetv2_w32
    #     #   hrnetv2_w48
    #     "backbone": "hrnetv2_w32",
    #     "input_shape": [480, 480],  # 输入图片的大小
    # }

    def __init__(self, **kwargs):
        # self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)

        self.model_path = 'logs/best_epoch_weights.h5'
        self.num_classes = 10  # 所需要区分的类的个数+1
        #  所使用的的主干网络： hrnetv2_w18 hrnetv2_w32 hrnetv2_w48
        self.backbone = "hrnetv2_w32"
        self.input_shape = [480, 480]  # 输入模型的图片尺寸
        self._defaults = {
            "model_path": self.model_path,
            "num_classes": self.num_classes,
            "backbone": self.backbone,
            "input_shape": self.input_shape,
        }

        if self.num_classes <= 21:
            # self.colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
            #                (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0),
            #                (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128), (0, 64, 0), (128, 64, 0),
            #                (0, 192, 0), (128, 192, 0), (0, 64, 128), (128, 64, 12)]
            self.colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                           (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0)]
        else:
            hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
            self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
            self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))

        #   加载模型
        self.model = HRnet([self.input_shape[0], self.input_shape[1], 3], self.num_classes, backbone=self.backbone)
        self.model.load_weights(self.model_path)
        logging.info('{} model loaded.'.format(self.model_path))
        show_config(**self._defaults)

    @tf.function
    def get_pred(self, photo):
        preds = self.model(photo, training=False)
        return preds

    #   检测图片
    def detect_image(self, image=None, name_classes=None, name_classes_gbk=None,
                     img_name=None, dir_save_path=None, result_txt=None):
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
                                  size=np.floor(3e-2 * image.size[1] + 20).astype('int32'))  # 修改字体大小
        draw = ImageDraw.Draw(image)
        classes_nums = np.zeros([self.num_classes])
        output_class_name = np.array([], dtype=int)  # 存放预测类别结果的数组
        for i in range(self.num_classes):
            num = np.sum(pr == i)
            if (num > 0) & (name_classes is not None):
                # draw.text((50 * i, 50 * i), str(name_classes_gbk[i]), fill='red', font=font)
                draw.text((50, 50 * i), str(name_classes_gbk[i]), fill='red', font=font)
                output_class_name = np.append(output_class_name, i)
            classes_nums[i] = num
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
            # 2023.4.25 读取预测出的所有类别 存放到numpy中
            for i in range(output_class_name.shape[0]):
                if output_class_name[i] > 0:
                    temp = output_class_name[i]
                    logging.info("识别出：{}--{}".format(temp, name_classes_gbk[temp]))
                    result_txt.write("    " + str(name_classes_gbk[temp]) + "\t")
            result_txt.write("\r")
            result_txt.write("  预测概率值最高的类别为： " + name_classes_gbk[max_output_class_name])
            result_txt.write("\r")
            image.save(os.path.join(dir_save_path, img_name))


def predict_main(mode=None, name_classes=None, name_classes_gbk=None, timeF=None):
    hrnet = HRNetSegmentation()
    if mode == 0:
        img_name = input('Input image filename:')
        image = Image.open(str(img_name))
        try:
            logging.info('success read image ' + str(img_name))
            filename, _ = os.path.splitext(img_name)
        except Exception as e:
            raise Exception(e)
        dir_save_path = str(filename) + "_img_out/"
        if not os.path.exists(dir_save_path):
            os.makedirs(dir_save_path)
        f1 = open(os.path.join(dir_save_path, str(filename) + '_predict_result.txt'), 'a', encoding='utf-8')
        logging.info("start image predict")
        hrnet.detect_image(image, name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                           img_name=img_name, dir_save_path=dir_save_path, result_txt=f1)
        f1.close()
        logging.info("success, predict done!")

    if mode == 1:
        video_name = input("Input video filename:")
        try:
            logging.info('success read video ' + str(video_name))
            filename, _ = os.path.splitext(video_name)
        except Exception as e:
            raise Exception(e)
        output_dir = str(filename) + '_img/'  # 保存图片文件夹路径
        output_img_type = '.jpg'  # 保存图片的格式
        vc = cv2.VideoCapture(video_name)
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
            if c % int(timeF) == 0:
                logging.info('success read frame No.' + str(c))
            c = c + 1
            cv2.waitKey(1)
        vc.release()
        # ------------------对img_out文件中图片批量预测
        logging.info("start video predict")
        dir_save_path = str(filename) + "_img_out/"
        if not os.path.exists(dir_save_path):
            os.makedirs(dir_save_path)
        img_names = os.listdir(output_dir)
        img_names.sort(key=lambda x: int(x.split('.')[0]))  # 按照1，2，3 顺序读图片
        f1 = open(os.path.join(dir_save_path, str(filename) + '_predict_result.txt'), 'a', encoding='utf-8')
        for img_name in tqdm(img_names):
            image_path = os.path.join(output_dir, img_name)
            image = Image.open(image_path)
            # 预测图片，只保存有预测结果图片
            hrnet.detect_image(image, name_classes=name_classes, name_classes_gbk=name_classes_gbk,
                               img_name=img_name, dir_save_path=dir_save_path, result_txt=f1)
        f1.close()
        logging.info("success, all predict done!")


if __name__ == "__main__":

    # 输入配置参数
    _mode, _use_gpu, _timeF = load_arg()

    # gpu or cpu 方式加载程序
    gpu_enable(_use_gpu=_use_gpu)

    # 读取标签文件
    _name_classes, _name_classes_gbk = read_txt_lines(_classes_txt=_classes_txt, _classes_gbk_txt=_classes_gbk_txt)

    # 进入预测 单张图片/视频
    predict_main(mode=int(_mode), name_classes=_name_classes, name_classes_gbk=_name_classes_gbk, timeF=_timeF)
