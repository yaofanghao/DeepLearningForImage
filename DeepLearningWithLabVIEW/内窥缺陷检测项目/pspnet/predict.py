import time
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from tqdm import tqdm

from pspnet import Pspnet

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
    
if __name__ == "__main__":
    #-------------------------------------------------------------------------#
    #   如果想要修改对应种类的颜色，到__init__函数里修改self.colors即可
    #-------------------------------------------------------------------------#
    pspnet = Pspnet()
    mode = "dir_predict"
    img_name = "test4_out_8bit.bmp"
    count           = False
    name_classes    = ["background","duoyuwu","aokeng","qipi","cashang","gubo","xiuban","baiban"]
    dir_origin_path = "img/"
    dir_save_path   = "img_out/"
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)

    if mode == "dir_predict":
        img_names = os.listdir(dir_origin_path)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path  = os.path.join(dir_origin_path, img_name)
                image       = Image.open(image_path)
                r_image     = pspnet.detect_image(image,name_classes=name_classes)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, img_name))
                
    else:
        raise AssertionError("Please specify the correct mode: 'predict', 'video', 'fps' or 'dir_predict'.")
