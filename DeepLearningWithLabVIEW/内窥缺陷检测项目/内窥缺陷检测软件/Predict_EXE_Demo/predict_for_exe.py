# 2023.3.7 @yaofanghao
# update 2023.4.7
# 用于制作exe的py文件

import time
import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
from tqdm import tqdm
import colorsys
import copy
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image,ImageFont,ImageDraw
from nets.hrnet import HRnet
from utils.utils import cvtColor, preprocess_input, resize_image, show_config

# 日志调试模块
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s',level=logging.DEBUG)

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

class HRnet_Segmentation(object):
    _defaults = {
        "model_path": 'logs/best_epoch_weights.h5',  # 模型权重
        "num_classes": 10,  # 所需要区分的类的个数+1
        # ----------------------------------------#
        #   所使用的的主干网络：
        #   hrnetv2_w18
        #   hrnetv2_w32
        #   hrnetv2_w48
        # ----------------------------------------#
        "backbone": "hrnetv2_w32",
        "input_shape": [480, 480],     #   输入图片的大小
    }

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
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
        #   获得模型
        self.generate()
        show_config(**self._defaults)

    #   获得所有的分类
    def generate(self):
        #   载入模型与权值
        self.model = HRnet([self.input_shape[0], self.input_shape[1], 3], self.num_classes, backbone=self.backbone)
        self.model.load_weights(self.model_path)
        logging.info('{} model loaded.'.format(self.model_path))

    @tf.function
    def get_pred(self, photo):
        preds = self.model(photo, training=False)
        return preds

    #   检测图片
    def detect_image(self, image, name_classes=None, img_name=None, filename=None):
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
        pr = pr[int((self.input_shape[0] - nh) // 2): int((self.input_shape[0] - nh) // 2 + nh), \
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
        output_class_name = np.array([0])  # 存放预测类别结果的数组
        for i in range(self.num_classes):
            num = np.sum(pr == i)
            if (num > 0) & (name_classes != None):
                draw.text((50 * i, 50 * i), str(name_classes[i]), fill='red', font=font)
                output_class_name = np.append(output_class_name, i)
            classes_nums[i] = num
        logging.debug( "{}发现缺陷--{}".format(img_name,output_class_name))
        max_output_class_name = np.max(output_class_name)

        # 2023.3.3改 只保存有预测结果的图片（只有background不算作有预测结果）
        # 代码原理：最大预测结果类别大于0，说明预测出的不是只有background，此时保存图片
        if (max_output_class_name > 0):
            f1 = open(os.path.join(os.getcwd(), 'predict_result.txt'), 'a')  # 存放预测结果的文件夹
            f1.write(img_name)
            f1.write("  最大分数预测类别为： "+ str(max_output_class_name))
            f1.write("\r")
            image.save(os.path.join( str(filename)+"_img_out/", img_name))
            f1.close()

if __name__ == "__main__":

    # ------------------输入要读取的内窥图像视频
    video_name = input("Input video filename:")
    try:
        logging.debug('success read video ' + str(video_name))
        filename, _ = os.path.splitext(video_name)
    except:
        logging.error('Fail to open video!')

    output_dir = str(filename) + '_img/'  # 保存图片文件夹路径
    output_img_type = '.jpg'  # 保存图片的格式
    vc = cv2.VideoCapture(video_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False
        logging.error('Video do not exist.')
    timeF = 1  # 视频帧计数间隔频率
    c = 1  # 统计帧数
    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if not rval:
            break
        if c % timeF == 0:  # 每隔timeF帧进行存储
            cv2.imwrite(output_dir + str(c) + output_img_type, frame)
            logging.debug('success read frame of video:' + str(c))
        c = c + 1
        cv2.waitKey(1)
    vc.release()
    
    # ------------------对img文件中图片批量预测
    logging.debug("-----------------------")
    logging.info("start model predict")
    hrnet = HRnet_Segmentation()
    name_classes    = ["background","duoyuwu","aokeng","qipi","cashang","gubo","xiuban","baiban","huashang","yanghuawu"]    #   区分的种类，和json_to_dataset里面的一样
    dir_save_path   = str(filename) + "_img_out/"
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)

    # localtime1 = time.localtime(time.time())
    img_names = os.listdir(output_dir)
    img_names.sort(key=lambda x : int(x.split('.')[0]))  # 按照1，2，3顺序读图片
    for img_name in tqdm(img_names):
        if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            image_path  = os.path.join(output_dir, img_name)
            image       = Image.open(image_path)
            # 预测图片，只保存有预测结果图片
            hrnet.detect_image(image, name_classes=name_classes, img_name=img_name, filename=filename)

    logging.info("success, all done")
