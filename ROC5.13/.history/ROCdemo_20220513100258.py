import os
import numpy as np
import tensorflow as tf
from PIL import Image
from pspnet import Pspnet
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
from sklearn import metrics
import matplotlib.pyplot as plt

if __name__ == "__main__":
    pspnet = Pspnet()
    #-----------------------------------------------
    # 需要根据具体情况设置：   

    # 三类 _background_ NEO NONNEO
    class_num = 1  # 0为背景,1为NEO,2为NONEO

    # 5.12 example: demo 非肿瘤 NONNEO 第二类
    #               demo2 肿瘤 NEO 第一类
    # dir_origin_path = "ROCtest/demo/"  # 示例，要评估ROC的jpg和png所在目录
    dir_origin_path = "ROCtest/demo2/"  

    img_name = '1.jpg'    # 要评估的jpg和png名称
    mask_name = '1.png'

    #------------------------------------------------

    image_path = os.path.join(dir_origin_path, img_name)
    image = Image.open(image_path)
    png_path = os.path.join(dir_origin_path, mask_name)
    png = Image.open(png_path)

    # pr 像素级别的预测概率，是一个三维tensor

    pr = pspnet.show_prob(image)
    pr = np.array(pr)

    # 制作预测为该类型概率的一维数组
    y_pred_num = []
    sum = 0
    for i in range(0,pr.shape[0]):
        for j in range(0,pr.shape[1]):
            y_pred_num.append(pr[i,j,class_num])
            sum+=1

    # print("pred_num is :",y_pred_num)
    # print(sum)

    # 制作真实标签的一维数组
    y_true = np.array(png)
    sum_true = 0
    y_true_num = []
    for i in range(0,y_true.shape[0]):
        for j in range(0,y_true.shape[1]):
            y_true_num.append(y_true[i,j,class_num])
            sum_true +=1

    # 将真实标签转换为布尔型 Ture or False
    y_true_num = np.array(y_true_num, dtype=bool)

    # dataframe格式列出
    # 像素值 | 对应类型的概率值
    # y_pred_num = np.concatenate(y_pred_num, axis=0)
    # y_true_num = np.concatenate(y_true_num, axis=0)

    # 绘制ROC曲线
    fpr, tpr, thresholds = metrics.roc_curve(y_true_num, y_pred_num)
    auc = metrics.auc(fpr, tpr)
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='AUC= %0.3f' % auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('ROC result')
    plt.legend(loc="lower right")
    plt.show()
    plt.savefig('roc-%s.png' %str(class_num))
    print("area under roc is: ", auc)