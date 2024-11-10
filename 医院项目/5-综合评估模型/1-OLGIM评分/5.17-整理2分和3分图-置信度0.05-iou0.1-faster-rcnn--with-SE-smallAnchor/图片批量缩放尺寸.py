"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/9/7 11:41
    @Filename: 图片批量缩放尺寸.py.py
    @Software: PyCharm     
"""
from PIL import Image
import os

# 定义目标尺寸
target_size = (800, 800)

# 指定图片文件夹路径
folder_path = 'img'

# 遍历文件夹中的图片文件
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # 拼接完整的文件路径
        file_path = os.path.join(folder_path, filename)

        # 打开图片
        image = Image.open(file_path)

        # 缩放图片
        resized_image = image.resize(target_size)

        # 保存缩放后的图片（覆盖原始图片）
        resized_image.save(file_path)
        print(filename)

print("图片缩放完成！")
