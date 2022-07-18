import os
# import imageio
from unet import Unet
from PIL import Image
import tensorflow as tf

# gpus = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpus[0], True)

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
        r_image.show()
        # imageio.imwrite(os.path.join(str2, filename), r_image)
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
