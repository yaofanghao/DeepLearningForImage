# 2023.2.15 批量对图片进行retinex图像增强，
# 目的是减少光照影响，提升训练集的图像质量
# 参考来源：https://github.com/dongb5/Retinex

import numpy as np
import cv2
import os
import json
import retinex


# 修改内容区域： 注意！！路径不能有中文！！！！
data_path = 'jpg'  # 原始图片文件夹名称
save_dir = "E:\\MyGithub\\0\\jpg2\\"  # 处理后图片路径
#######################

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

img_list = os.listdir(data_path)
if len(img_list) == 0:
    print('Data directory is empty.')
    exit()

with open('config.json', 'r') as f:
    config = json.load(f)

for i in img_list:
    print(i)
    filename, extension = os.path.splitext(i)

    # 读取图像
    img = cv2.imread(os.path.join(data_path, i), cv2.IMREAD_COLOR)

    # retinex图像增强模块--共有三种方法
    img_msrcr = retinex.MSRCR(
        img,
        config['sigma_list'],
        config['G'],
        config['b'],
        config['alpha'],
        config['beta'],
        config['low_clip'],
        config['high_clip']
    )

    img_amsrcr = retinex.automatedMSRCR(
        img,
        config['sigma_list']
    )

    img_msrcp = retinex.MSRCP(
        img,
        config['sigma_list'],
        config['low_clip'],
        config['high_clip']
    )

    # 按照特定格式保存图片
    save_path1 = save_dir + str(filename) + '_retinex.jpg'
    save_path2 = save_dir + str(filename) + '_auto_retinex.jpg'
    save_path3 = save_dir + str(filename) + '_MSRCP.jpg'
    cv2.imwrite(save_path1, img_msrcr)
    cv2.imwrite(save_path2, img_amsrcr)
    cv2.imwrite(save_path3, img_msrcp)