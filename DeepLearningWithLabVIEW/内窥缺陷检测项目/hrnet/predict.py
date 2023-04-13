import time

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

from hrnet import HRnet_Segmentation

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

if __name__ == "__main__":
    hrnet = HRnet_Segmentation()
    mode = "predict"
    name_classes    = ["background","duoyuwu","aokeng","qipi","cashang","gubo","xiuban","baiban","huashang","yanghuawu"]    #   区分的种类，和json_to_dataset里面的一样
    dir_origin_path = "img/"
    dir_save_path   = "img_out/"

    if mode == "predict":
        while True:
            img = input('Input image filename:')
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image = hrnet.detect_image(image, name_classes=name_classes)
                r_image.show()
        
    if mode == "dir_predict":
        import os
        from tqdm import tqdm

        img_names = os.listdir(dir_origin_path)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path  = os.path.join(dir_origin_path, img_name)
                image       = Image.open(image_path)
                r_image     = hrnet.detect_image(image, name_classes=name_classes)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, img_name))
