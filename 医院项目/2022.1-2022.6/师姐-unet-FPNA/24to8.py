from PIL import Image
import numpy as np
import cv2
import os



# 批量转换图片位深度
# path = r'./miou_pr_dir//'
# save_path = r'./miou_pr_dir//'
path = r'./VOCdevkit/VOC2007/SegmentationClass//'
save_path = r'./VOCdevkit/VOC2007/SegmentationClass//'
for i in os.listdir(path):
    img = Image.open(path+i)
    img = Image.fromarray(np.uint8(img))
    t = img.convert('L')
    img = Image.fromarray(np.uint8(t))  # *255
    img.save(save_path+i)
    print(1)
print('success')
