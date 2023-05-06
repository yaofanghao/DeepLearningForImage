# coding=utf-8
import os
from model import resolve_single
from model.srgan import generator
import cv2
from PIL import Image
import numpy

if __name__ == '__main__':
    # 加载模型
    weights_dir = 'weights'
    weights_file = lambda filename: os.path.join(weights_dir, filename)
    os.makedirs(weights_dir, exist_ok=True)
    pre_generator = generator()
    gan_generator = generator()
    pre_generator.load_weights(weights_file('pre_generator.h5'))
    gan_generator.load_weights(weights_file('gan_generator.h5'))

    #目标文件夹路径
    determination = './data'
    if not os.path.exists(determination):
        os.makedirs(determination)

    #原文件夹总的路径
    path = './data'
    folders = os.listdir(path)

    flag = 0
    for folder in folders:
        dirs = path + '/' + str(folder)
        dirs_dir = os.listdir(dirs)
        for file in dirs_dir:
            source = dirs + '/' + str(file)

            # source 原图所在路径
            # deter 处理后图片保存路径
            image = numpy.array(Image.open(source))
            if (image.shape[0] >= image.shape[1]):
                dst_shape0 = 1280
                dst_shape1 = 720
                pre_sr = resolve_single(pre_generator, image)
                gan_sr = resolve_single(gan_generator, image)
                pre_sr_array = pre_sr.numpy()
                # plt.imsave("pre_sr.png", pre_sr_array)
                image2 = cv2.resize(pre_sr_array, (dst_shape1, dst_shape0), interpolation=cv2.INTER_LANCZOS4)
            else:
                dst_shape0 = 720
                dst_shape1 = 1280
                pre_sr = resolve_single(pre_generator, image)
                gan_sr = resolve_single(gan_generator, image)
                pre_sr_array = pre_sr.numpy()
                image2 = cv2.resize(pre_sr_array, (dst_shape1, dst_shape0), interpolation=cv2.INTER_LANCZOS4)
            deter_dir = determination + '/' + str(folder)
            if not os.path.exists(deter_dir):
                os.makedirs(deter_dir)
            deter = deter_dir + '/' + str(file)
            print("image source is:", source)
            print("image save to:", deter)
            image2 = Image.fromarray(image2.astype('uint8')).convert('RGB')
            image2.save(deter)
            flag = flag+1
            print("success, number is ", flag)




