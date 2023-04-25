from PIL import Image
import numpy as np
import cv2
import os

# 原图是24位
img_name = 'test3.bmp'
img_out_name = 'test3_out_8bit.bmp'

img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

# 转换图片位深度24 to 8
# img = Image.open(img)
img = Image.fromarray(np.uint8(img))
t = img.convert('L')
img = Image.fromarray(np.uint8(t))  # *255
img.save(img_out_name)

print('success')