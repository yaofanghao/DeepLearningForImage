# 2023.4.11 @yaofanghao
# 几种超分辨率算法对比 
# coding=utf-8
import os
from model import resolve_single
from model.srgan import generator
import cv2
from PIL import Image
import numpy

# ------------------ 超分辨率算法模式
# 1 只有lanczos
# 2 只有srgan_pre_sr
# 3 只有srgan_gan_sr
# 4 srgan_pre_sr融合lanczos
# mode = 1 

if __name__ == '__main__':    
    mode = input("Input processing mode:")
    try:
        print('Input mode is ' + str(mode))
        mode = int(mode)
    except:
        raise AssertionError('Mode is incorret!')  
       
    if(mode==1):
        pass
    else:
        # 加载模型
        weights_dir = 'weights'
        weights_file = lambda filename: os.path.join(weights_dir, filename)
        os.makedirs(weights_dir, exist_ok=True)
        pre_generator = generator()
        gan_generator = generator()
        pre_generator.load_weights(weights_file('pre_generator.h5'))
        gan_generator.load_weights(weights_file('gan_generator.h5'))
    
    #原文件夹总的路径
    path = './jpg'
    folders = os.listdir(path)

    #目标文件夹路径
    if(mode==1):
        determination = './lanczos_output'
    if(mode==2):
        determination = './presr_output'
    if(mode==3):
        determination = './gansr_output'
    if(mode==4):
        determination = './presr_lanczos_output'
    if not os.path.exists(determination):
        os.makedirs(determination)

    flag = 0
    for folder in folders:
        source = path + '/' + str(folder)

        # source 原图所在路径
        # deter 处理后图片保存路径
        image = numpy.array(Image.open(source))
        dst_shape0 = image.shape[0]*4
        dst_shape1 = image.shape[1]*4

        # 图像处理模块
        if(mode==1):
            image2 = cv2.resize(image, (dst_shape1, dst_shape0), interpolation=cv2.INTER_LANCZOS4)
        if(mode==2):
            pre_sr = resolve_single(pre_generator, image)
            image2 = pre_sr.numpy()
        if(mode==3):
            gan_sr = resolve_single(gan_generator, image)
            image2 = gan_sr.numpy()
        if(mode==4):
            pre_sr = resolve_single(pre_generator, image)
            pre_sr_array = pre_sr.numpy()
            image2 = cv2.resize(pre_sr_array, (dst_shape1, dst_shape0), interpolation=cv2.INTER_LANCZOS4)
        
        deter = determination + '/' + str(folder)        
        image2 = Image.fromarray(image2.astype('uint8')).convert('RGB')
        image2.save(deter)
        flag = flag+1
        print("No.%d, image source is:%s, save to:%s success!" %(flag,source,deter))




