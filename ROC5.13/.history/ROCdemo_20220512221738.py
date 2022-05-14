
5.12 待修改 细节部分调整

import os
import time
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from pspnet import Pspnet
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
from tqdm import tqdm
pspnet = Pspnet()

dir_origin_path = "ROCtest/demo/"
# dir_save_path = 'ROCtest/demo/predict/'

img_name = '1.jpg'
mask_name = '1.png'

image_path = os.path.join(dir_origin_path, img_name)
image = Image.open(image_path)

png_path = os.path.join(dir_origin_path, mask_name)
png = Image.open(png_path)

# 显示像素级别的预测概率，是一个三维tensor
# 三类 _background_ NEO NONNEO
# example: 丛玉珍 非肿瘤 NONNEO 第二类

pr = pspnet.show_prob(image)
pr

pr = np.array(pr)
pr.shape

pr.shape[1]

class_num = 2 # 1为NEO，2为NONEO

y_pred_num = []

sum = 0
for i in range(0,pr.shape[0]):
    for j in range(0,pr.shape[1]):
        y_pred_num.append(pr[i,j,class_num])
        sum+=1

y_pred_num
# print("pred_num is :",y_pred_num)
# print(sum)

# 真实标签图
y_true = np.array(png)
y_true

sum_true = 0

y_true_num = []
for i in range(0,y_true.shape[0]):
    for j in range(0,y_true.shape[1]):
        y_true_num.append(y_true[i,j,class_num])
        sum_true +=1

# y_true_num[y_true_num==class_num] = 1

y_true_num = np.array(y_true_num, dtype=bool)

y_true_num

# sum_true

np.array(y_pred_num).shape

# dataframe格式列出
# 像素值 | 对应类型的概率值

# y_pred_num = np.concatenate(y_pred_num, axis=0)

# y_true_num = np.concatenate(y_true_num, axis=0)


# 绘制ROC曲线

from sklearn import metrics 
fpr, tpr, thresholds = metrics.roc_curve(y_true_num, y_pred_num)

auc = metrics.auc(fpr, tpr)
auc

import matplotlib.pyplot as plt

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC result')
plt.legend(loc="lower right")
plt.show()
