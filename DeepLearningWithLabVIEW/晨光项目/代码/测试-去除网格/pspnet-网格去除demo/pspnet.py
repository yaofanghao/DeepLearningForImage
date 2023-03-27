import colorsys
import copy
import time

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

from nets.pspnet import pspnet
from utils.utils import cvtColor, preprocess_input, resize_image, show_config

class Pspnet(object):
    _defaults = {
        "model_path"        : 'best_epoch_weights.h5',
        "num_classes"       : 2,
        "backbone"          : "resnet50",
        "input_shape"       : [473, 473],
        "downsample_factor" : 8,
        "mix_type"          : 1,
    }

    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        for name, value in kwargs.items():
            setattr(self, name, value)
        if self.num_classes <= 21:
            self.colors = [  (0, 0, 0), (255, 255, 255)]  # 网格为白，其他为黑
        else:
            hsv_tuples = [(x / self.num_classes, 1., 1.) for x in range(self.num_classes)]
            self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
            self.colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), self.colors))

        self.generate()
        show_config(**self._defaults)

    def generate(self):
        self.model = pspnet([self.input_shape[0], self.input_shape[1], 3], self.num_classes,
                    downsample_factor=self.downsample_factor, backbone=self.backbone, aux_branch=False)
        self.model.load_weights(self.model_path, by_name = True)
        print('pspnet model start...')
        print('{} model loaded.'.format(self.model_path))

    @tf.function
    def get_pred(self, image_data):
        pr = self.model(image_data, training=False)
        return pr

    def detect_image(self, image, count=False, name_classes=None):
        image       = cvtColor(image)
        old_img     = copy.deepcopy(image)
        orininal_h  = np.array(image).shape[0]
        orininal_w  = np.array(image).shape[1]

        image_data, nw, nh  = resize_image(image, (self.input_shape[1], self.input_shape[0]))
        image_data  = np.expand_dims(preprocess_input(np.array(image_data, np.float32)), 0)

        pr = self.get_pred(image_data)[0].numpy()
        pr = pr[int((self.input_shape[0] - nh) // 2) : int((self.input_shape[0] - nh) // 2 + nh), \
                int((self.input_shape[1] - nw) // 2) : int((self.input_shape[1] - nw) // 2 + nw)]
        pr = cv2.resize(pr, (orininal_w, orininal_h), interpolation = cv2.INTER_LINEAR)
        pr = pr.argmax(axis=-1)

        seg_img = np.reshape(np.array(self.colors, np.uint8)[np.reshape(pr, [-1])], [orininal_h, orininal_w, -1])
        image   = Image.fromarray(np.uint8(seg_img))  
        return image