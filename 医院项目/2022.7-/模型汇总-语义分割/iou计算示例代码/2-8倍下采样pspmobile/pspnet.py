import colorsys
import copy
import time

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

from nets.pspnet import pspnet
from utils.utils import cvtColor, preprocess_input, resize_image


#--------------------------------------------#
#   使用自己训练好的模型预测需要修改3个参数
#   model_path、backbone和num_classes都需要修改！
#   如果出现shape不匹配
#   一定要注意训练时的model_path、
#   backbone和num_classes数的修改
#--------------------------------------------#
class Pspnet(object):
    _defaults = {
        #-------------------------------------------------------------------#
        #   model_path指向logs文件夹下的权值文件
        #   训练好后logs文件夹下存在多个权值文件，选择验证集损失较低的即可。
        #   验证集损失较低不代表miou较高，仅代表该权值在验证集上泛化性能较好。
        #-------------------------------------------------------------------#
        "model_path"        : 'logs/ep136-loss0.243-val_loss0.318.h5',
        #----------------------------------------#
        #   所需要区分的类的个数+1
        #----------------------------------------#
        "num_classes"       : 2,
        #----------------------------------------#
        #   所使用的的主干网络：mobilenet、resnet50
        #----------------------------------------#
        "backbone"          : "mobilenet",
        #----------------------------------------#
        #   输入图片的大小
        #----------------------------------------#
        "input_shape"       : [473, 473],
        #----------------------------------------#
        #   下采样的倍数，一般可选的为8和16
        #   与训练时设置的一样即可
        #----------------------------------------#
        "downsample_factor" : 16,
        #-------------------------------------------------#
        #   mix_type参数用于控制检测结果的可视化方式
        #
        #   mix_type = 0的时候代表原图与生成的图进行混合
        #   mix_type = 1的时候代表仅保留生成的图
        #   mix_type = 2的时候代表仅扣去背景，仅保留原图中的目标
        #-------------------------------------------------#
        "mix_type"          : 0,
    }

    #---------------------------------------------------#
    #   初始化PSPNET
    #---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
        #---------------------------------------------------#
        #   画框设置不同的颜色
        #---------------------------------------------------#
        if self.num_classes <= 21:
            self.colors = [ (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128), (0, 128, 128), 
                            (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0), (192, 128, 0), (64, 0, 128), (192, 0, 128), 
                            (64, 128, 128), (192, 128, 128), (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128), 
                            (128, 64, 12)]
        else:
            hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
            self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
            self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))
        #---------------------------------------------------#
        #   获得模型
        #---------------------------------------------------#
        self.generate()

    #---------------------------------------------------#
    #   载入模型
    #---------------------------------------------------#
    def generate(self):
        #-------------------------------#
        #   载入模型与权值
        #-------------------------------#
        self.model = pspnet([self.input_shape[0], self.input_shape[1], 3], self.num_classes,
                    downsample_factor=self.downsample_factor, backbone=self.backbone, aux_branch=False)
        self.model.load_weights(self.model_path, by_name = True)
        print('{} model loaded.'.format(self.model_path))

    @tf.function
    def get_pred(self, image_data):
        pr = self.model(image_data, training=False)
        return pr
    #---------------------------------------------------#
    #   检测图片
    #---------------------------------------------------#
    def detect_image(self, image):
        #---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        #---------------------------------------------------------#
        image       = cvtColor(image)
        #---------------------------------------------------#
        #   对输入图像进行一个备份，后面用于绘图
        #---------------------------------------------------#
        old_img     = copy.deepcopy(image)
        orininal_h  = np.array(image).shape[0]
        orininal_w  = np.array(image).shape[1]
        #---------------------------------------------------------#
        #   给图像增加灰条，实现不失真的resize
        #   也可以直接resize进行识别 
        #---------------------------------------------------------#
        image_data, nw, nh  = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        #---------------------------------------------------------#
        #   归一化+通道数调整到第一维度+添加上batch_size维度
        #---------------------------------------------------------#
        image_data  = np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0)

        #---------------------------------------------------#
        #   图片传入网络进行预测
        #---------------------------------------------------#
        pr = self.get_pred(image_data)[0].numpy()
        #---------------------------------------------------#
        #   将灰条部分截取掉
        #---------------------------------------------------#
        pr = pr[int((self.input_shape[0] - nh) // 2) : int((self.input_shape[0] - nh) // 2 + nh), \
                int((self.input_shape[1] - nw) // 2) : int((self.input_shape[1] - nw) // 2 + nw)]
        #---------------------------------------------------#
        #   进行图片的resize
        #---------------------------------------------------#
        pr = cv2.resize(pr, (orininal_w, orininal_h), interpolation = cv2.INTER_LINEAR)
        #---------------------------------------------------#
        #   取出每一个像素点的种类
        #---------------------------------------------------#
        pr = pr.argmax(axis=-1)

        if self.mix_type == 0:
            # seg_img = np.zeros((np.shape(pr)[0], np.shape(pr)[1], 3))
            # for c in range(self.num_classes):
            #     seg_img[:, :, 0] += ((pr[:, :] == c ) * self.colors[c][0]).astype('uint8')
            #     seg_img[:, :, 1] += ((pr[:, :] == c ) * self.colors[c][1]).astype('uint8')
            #     seg_img[:, :, 2] += ((pr[:, :] == c ) * self.colors[c][2]).astype('uint8')
            seg_img = np.reshape(np.array(self.colors, np.uint8)[np.reshape(pr, [-1])], [orininal_h, orininal_w, -1])
            #------------------------------------------------#
            #   将新图片转换成Image的形式
            #------------------------------------------------#
            image   = Image.fromarray(np.uint8(seg_img))
            #------------------------------------------------#
            #   将新图与原图及进行混合
            #------------------------------------------------#
            image   = Image.blend(old_img, image, 0.7)

        elif self.mix_type == 1:
            # seg_img = np.zeros((np.shape(pr)[0], np.shape(pr)[1], 3))
            # for c in range(self.num_classes):
            #     seg_img[:, :, 0] += ((pr[:, :] == c ) * self.colors[c][0]).astype('uint8')
            #     seg_img[:, :, 1] += ((pr[:, :] == c ) * self.colors[c][1]).astype('uint8')
            #     seg_img[:, :, 2] += ((pr[:, :] == c ) * self.colors[c][2]).astype('uint8')
            seg_img = np.reshape(np.array(self.colors, np.uint8)[np.reshape(pr, [-1])], [orininal_h, orininal_w, -1])
            #------------------------------------------------#
            #   将新图片转换成Image的形式
            #------------------------------------------------#
            image   = Image.fromarray(np.uint8(seg_img))

        elif self.mix_type == 2:
            seg_img = (np.expand_dims(pr != 0, -1) * np.array(old_img, np.float32)).astype('uint8')
            #------------------------------------------------#
            #   将新图片转换成Image的形式
            #------------------------------------------------#
            image = Image.fromarray(np.uint8(seg_img))
        
        return image

    def get_FPS(self, image, test_interval):
        #---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        #---------------------------------------------------------#
        image       = cvtColor(image)
        #---------------------------------------------------------#
        #   给图像增加灰条，实现不失真的resize
        #   也可以直接resize进行识别 
        #---------------------------------------------------------#
        image_data, nw, nh  = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        #---------------------------------------------------------#
        #   归一化+通道数调整到第一维度+添加上batch_size维度
        #---------------------------------------------------------#
        image_data  = np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0)

        #---------------------------------------------------#
        #   图片传入网络进行预测
        #---------------------------------------------------#
        pr = self.get_pred(image_data)[0].numpy()
        #---------------------------------------------------#
        #   取出每一个像素点的种类
        #---------------------------------------------------#
        pr = pr.argmax(axis=-1).reshape([self.input_shape[0],self.input_shape[1]])
        #--------------------------------------#
        #   将灰条部分截取掉
        #--------------------------------------#
        pr = pr[int((self.input_shape[0] - nh) // 2) : int((self.input_shape[0] - nh) // 2 + nh), \
                int((self.input_shape[1] - nw) // 2) : int((self.input_shape[1] - nw) // 2 + nw)]
                
        t1 = time.time()
        for _ in range(test_interval):
            #---------------------------------------------------#
            #   图片传入网络进行预测
            #---------------------------------------------------#
            pr = self.get_pred(image_data)[0].numpy()
            #---------------------------------------------------#
            #   取出每一个像素点的种类
            #---------------------------------------------------#
            pr = pr.argmax(axis=-1).reshape([self.input_shape[0],self.input_shape[1]])
            #--------------------------------------#
            #   将灰条部分截取掉
            #--------------------------------------#
            pr = pr[int((self.input_shape[0] - nh) // 2) : int((self.input_shape[0] - nh) // 2 + nh), \
                    int((self.input_shape[1] - nw) // 2) : int((self.input_shape[1] - nw) // 2 + nw)]

        t2 = time.time()
        tact_time = (t2 - t1) / test_interval
        return tact_time
        
    def get_miou_png(self, image):
        #---------------------------------------------------------#
        #   在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        #---------------------------------------------------------#
        image       = cvtColor(image)
        orininal_h  = np.array(image).shape[0]
        orininal_w  = np.array(image).shape[1]
        #---------------------------------------------------------#
        #   给图像增加灰条，实现不失真的resize
        #   也可以直接resize进行识别 
        #---------------------------------------------------------#
        image_data, nw, nh  = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        #---------------------------------------------------------#
        #   归一化+通道数调整到第一维度+添加上batch_size维度
        #---------------------------------------------------------#
        image_data  = np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0)

        #---------------------------------------------------#
        #   图片传入网络进行预测
        #---------------------------------------------------#
        pr = self.get_pred(image_data)[0].numpy()
        #--------------------------------------#
        #   将灰条部分截取掉
        #--------------------------------------#
        pr = pr[int((self.input_shape[0] - nh) // 2) : int((self.input_shape[0] - nh) // 2 + nh), \
                int((self.input_shape[1] - nw) // 2) : int((self.input_shape[1] - nw) // 2 + nw)]
        #--------------------------------------#
        #   进行图片的resize
        #--------------------------------------#
        pr = cv2.resize(pr, (orininal_w, orininal_h), interpolation = cv2.INTER_LINEAR)
        #---------------------------------------------------#
        #   取出每一个像素点的种类
        #---------------------------------------------------#
        pr = pr.argmax(axis=-1)

        image = Image.fromarray(np.uint8(pr))
        return image
