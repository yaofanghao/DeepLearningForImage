from PIL import Image
from unet import Unet
import os

# gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)

def count(path):  #统计文件夹内图片个数的函数
    i = 0
    for root, dirs, files in os.walk(path):
        for each in files:
            if each.endswith('jpg'):
                i += 1
    return i

if __name__ == "__main__":

    img = "./img"
    img_out = "./img_out"

    if not os.path.exists(img):
        os.makedirs(img)
    if not os.path.exists(img_out):
        os.makedirs(img_out)

    unet = Unet()
    for i in range(1, count(img)+1):
        image_path = (img + '/' + str(i) +".jpg")
        try:
            image = Image.open(image_path)
        except:
            print('Open Error! Try again!')
            break
        else:
            image = unet.detect_image(image)

            image.save (img_out + '/' + str(i) + ".jpg")
