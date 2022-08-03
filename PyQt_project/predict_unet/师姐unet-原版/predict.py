import os
import imageio
from unet import Unet
from PIL import Image
import tensorflow as tf

# gpus = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpus[0], True)

#f = open(r"E:\登陆系统重写\待检测文件路径.txt", 'r')
#str1 = f.read()
#f1 = open(r"E:\登陆系统重写\保存文件路径.txt", 'r')
#str2 = f1.read()
str1="E:\PycharmProjects\TensorFlow\PyQt_project\predict_unet\师姐unet-原版\\img"
str2="E:\PycharmProjects\TensorFlow\PyQt_project\predict_unet\师姐unet-原版\\img_out"

if not os.path.exists(str2):
    os.makedirs(str2)

unet = Unet()
count = os.listdir(str1)
for filename in count:
    img = filename
    try:
        image = Image.open(os.path.join(str1, img))
    except:
        print('Open Error! Try again!')
        continue
    else:

        r_image = unet.detect_image(image)
        imageio.imwrite(os.path.join(str2, filename), r_image)
pass

# -------------------------------------#
#       对单张图片进行预测
# -------------------------------------#
# import os
#
# import imageio
#
# from unet import Unet
# from PIL import Image
# import tensorflow as tf
# gpus = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpus[0], True)
# unet = Unet()
#
#
# count=os.listdir("C:\\Users\\admin\\Desktop\\image1")
# for filename in count:
#     img=filename
#
#     try:
#         # print(os.path.join(count, img))
#         image = Image.open(os.path.join("C:\\Users\\admin\\Desktop\\image1", img))
#     except:
#         print('Open Error! Try again!')
#         continue
#     else:
#         r_image = unet.detect_image(image)
#         # r_image.imwrite("D:\\qiukaili\\unet-keras-master（迭代100次）\\unet-keras-master（裁剪） - 副本\\pr",filename)
#         imageio.imwrite(os.path.join('C:\\Users\\admin\\Desktop\\预测（裁剪）',
#                                      filename), r_image)
