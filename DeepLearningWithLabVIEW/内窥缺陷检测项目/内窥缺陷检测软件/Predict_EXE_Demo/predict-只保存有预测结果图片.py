import time
import os
from tqdm import tqdm

import colorsys
import copy
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image,ImageFont,ImageDraw
from nets.hrnet import HRnet
from utils.utils import cvtColor, preprocess_input, resize_image, show_config

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

class HRnet_Segmentation(object):
    _defaults = {
        "model_path": 'logs/best_epoch_weights.h5',
        "num_classes": 8,  # 所需要区分的类的个数+1
        # ----------------------------------------#
        #   所使用的的主干网络：
        #   hrnetv2_w18
        #   hrnetv2_w32
        #   hrnetv2_w48
        # ----------------------------------------#
        "backbone": "hrnetv2_w32",
        # ----------------------------------------#
        #   输入图片的大小
        # ----------------------------------------#
        # "input_shape": [480, 480],
        "input_shape": [320, 320],
    }

    # ---------------------------------------------------#
    #   初始化Deeplab
    # ---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
        # ---------------------------------------------------#
        #   画框设置不同的颜色
        # ---------------------------------------------------#
        if self.num_classes <= 21:
            self.colors = [(0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                           (0, 128, 128),
                           (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0), (64, 0, 128),
                           (192, 0, 128),
                           (64, 128, 128), (192, 128, 128), (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0),
                           (0, 64, 128),
                           (128, 64, 12)]
        else:
            hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
            self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
            self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))
        # ---------------------------------------------------#
        #   获得模型
        # ---------------------------------------------------#
        self.generate()
        show_config(**self._defaults)

    # ---------------------------------------------------#
    #   获得所有的分类
    # ---------------------------------------------------#
    def generate(self):
        # -------------------------------#
        #   载入模型与权值
        # -------------------------------#
        self.model = HRnet([self.input_shape[0], self.input_shape[1], 3], self.num_classes, backbone=self.backbone)

        self.model.load_weights(self.model_path)
        print('{} model loaded.'.format(self.model_path))

    @tf.function
    def get_pred(self, photo):
        preds = self.model(photo, training=False)
        return preds

    # ---------------------------------------------------#
    #   检测图片
    # ---------------------------------------------------#
    def detect_image(self, image, name_classes=None, img_name=None):
        # ---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        # ---------------------------------------------------------#
        image = cvtColor(image)
        # ---------------------------------------------------#
        #   对输入图像进行一个备份，后面用于绘图
        # ---------------------------------------------------#
        old_img = copy.deepcopy(image)
        orininal_h = np.array(image).shape[0]
        orininal_w = np.array(image).shape[1]
        # ---------------------------------------------------------#
        #   给图像增加灰条，实现不失真的resize
        # ---------------------------------------------------------#
        image_data, nw, nh = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        # ---------------------------------------------------------#
        #   归一化+添加上batch_size维度
        # ---------------------------------------------------------#
        image_data = np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0)

        # ---------------------------------------------------#
        #   图片传入网络进行预测
        # ---------------------------------------------------#
        pr = self.get_pred(image_data)[0].numpy()
        # ---------------------------------------------------#
        #   将灰条部分截取掉
        # ---------------------------------------------------#
        pr = pr[int((self.input_shape[0] - nh) // 2): int((self.input_shape[0] - nh) // 2 + nh), \
             int((self.input_shape[1] - nw) // 2): int((self.input_shape[1] - nw) // 2 + nw)]
        # ---------------------------------------------------#
        #   进行图片的resize
        # ---------------------------------------------------#
        pr = cv2.resize(pr, (orininal_w, orininal_h), interpolation=cv2.INTER_LINEAR)
        # ---------------------------------------------------#
        #   取出每一个像素点的种类
        # ---------------------------------------------------#
        pr = pr.argmax(axis=-1)

        # seg_img = np.zeros((np.shape(pr)[0], np.shape(pr)[1], 3))
        # for c in range(self.num_classes):
        #     seg_img[:, :, 0] += ((pr[:, :] == c ) * self.colors[c][0]).astype('uint8')
        #     seg_img[:, :, 1] += ((pr[:, :] == c ) * self.colors[c][1]).astype('uint8')
        #     seg_img[:, :, 2] += ((pr[:, :] == c ) * self.colors[c][2]).astype('uint8')
        seg_img = np.reshape(np.array(self.colors, np.uint8)[np.reshape(pr, [-1])], [orininal_h, orininal_w, -1])
        image = Image.fromarray(np.uint8(seg_img))
        image = Image.blend(old_img, image, 0.7)

        # 修改显示字体
        font = ImageFont.truetype(font='model_data/simhei.ttf',
                                  size=np.floor(3e-2 * image.size[1] + 20).astype('int32'))  # 修改字体大小
        draw = ImageDraw.Draw(image)
        classes_nums = np.zeros([self.num_classes])
        total_points_num = orininal_h * orininal_w
        # print('-' * 63)
        # print("|%25s | %15s | %15s|" % ("Key", "Value", "Ratio"))
        # print('-' * 63)
        output_class_name = np.array([0])  # 存放预测类别结果的数组
        for i in range(self.num_classes):
            num = np.sum(pr == i)
            ratio = num / total_points_num * 100
            if (num > 0) & (name_classes != None):
                # print("|%25s | %15s | %14.2f%%|"%(str(name_classes[i]), str(num), ratio))
                # print('-' * 63)
                draw.text((50 * i, 50 * i), str(name_classes[i]), fill='red', font=font)
                output_class_name = np.append(output_class_name, i)
            classes_nums[i] = num
        # print("classes_nums:", classes_nums)
        #  (img_name, "--", output_class_name)
        max_output_class_name = np.max(output_class_name)
        # print("max: ", max_output_class_name)

        # 2023.3.3 只保存有预测结果的图片（只有background不算作有预测结果）
        # 最大预测结果类别大于0，说明预测出的不是只有background
        if (max_output_class_name > 0):
            # f1.write(img_name)
            # f1.write("\r")
            # f1.write(max_output_class_name)
            # f1.write("\r")
            image.save(os.path.join("img_out/", img_name))

if __name__ == "__main__":
    hrnet1 = HRnet_Segmentation()
    name_classes    = ["background","duoyuwu","aokeng","qipi","cashang","gubo","xiuban","baiban"]    #   区分的种类，和json_to_dataset里面的一样
    dir_origin_path = "img/"
    dir_save_path   = "img_out/"
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)
    # f1 = open(os.path.join(os.getcwd(), 'predict_result.txt'), 'a')

    localtime1 = time.localtime(time.time())
    img_names = os.listdir(dir_origin_path)
    img_names.sort(key=lambda x:int(x.split('.')[0]))  # 按照1，2，3顺序读图片
    for img_name in tqdm(img_names):
        if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            image_path  = os.path.join(dir_origin_path, img_name)
            image       = Image.open(image_path)
            hrnet1.detect_image(image, name_classes=name_classes, img_name=img_name)

    localtime2 = time.localtime(time.time())
    print("begin time: ", localtime1)
    print("end time: ", localtime2)