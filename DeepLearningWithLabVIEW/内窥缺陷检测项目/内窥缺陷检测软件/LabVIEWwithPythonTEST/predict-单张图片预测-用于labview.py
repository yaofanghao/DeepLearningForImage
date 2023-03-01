# 2023.3.1 针对labview调用的predict.py和hrnet.py
# 将predict封装为一个函数，在labview中调用，输入为img，输出为r_image和res

import tensorflow as tf
from PIL import Image

from hrnet import HRnet_Segmentation

gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

def predict(img):
    hrnet = HRnet_Segmentation()
    name_classes = ["background","duoyuwu","aokeng","qipi","cashang","gubo","xiuban","baiban"]
    # img = input('Input image filename:')
    image = Image.open(img)
    r_image, res = hrnet.detect_image(image, name_classes=name_classes)
    return r_image, res

if __name__ == "__main__":
    img = "1.jpg"
    r_image,res = predict(img)
    r_image.show()
    r_image.save("out.jpg")
    print("result:", res)
    print("success!")