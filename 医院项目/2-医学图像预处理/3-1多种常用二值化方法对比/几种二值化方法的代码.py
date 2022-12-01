# https://blog.csdn.net/weixin_38757163/article/details/123704622

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# 平均值法
def mean_binarization(img_gray):
    threshold = np.mean(img_gray)
    img_gray[img_gray>threshold] = 255
    img_gray[img_gray<=threshold] = 0
    # For displaying a grayscale image set up the colormapping using the parameters cmap='gray', vmin=0, vmax=255.
    # plt.imshow(img_gray, cmap='gray')
    # plt.show()
    return img_gray

# 双峰法
def hist_binarization(img_gray):
    hist = img_gray.flatten()
    plt.subplot(121)
    plt.hist(hist, 256)
    cnt_hist = Counter(hist)
    most_commons = cnt_hist.most_common(2)
    # get the grey values of bimodal histogram
    begin, end = most_commons[0][0], most_commons[1][0]
    if begin > end:
        begin, end = end, begin
    print("双峰法测试....")
    print(f'{begin}: {end}')
    cnt = np.iinfo(np.int16).max
    threshold = 0
    for i in range(begin, end+1):
        if cnt_hist[i] < cnt:
            cnt = cnt_hist[i]
            threshold = i
    print(f'{threshold}: {cnt}')
    img_gray[img_gray>threshold] = 255
    img_gray[img_gray<=threshold] = 0
    # plt.subplot(122)
    # plt.imshow(img_gray, cmap='gray')
    # plt.show()
    return img_gray

base_dir = "./jpg"
out_gray_dir = "./gray/"
output_erzhihua_dir = './erzhihua/'
output_otsu_dir = './otsu/'
output_hist_dir = './hist/'
output_mean_dir = "./mean/"

if not os.path.exists(output_otsu_dir):
    os.makedirs(output_otsu_dir)
if not os.path.exists(output_erzhihua_dir):
    os.makedirs(output_erzhihua_dir)
if not os.path.exists(output_mean_dir):
    os.makedirs(output_mean_dir)
if not os.path.exists(out_gray_dir):
    os.makedirs(out_gray_dir)
if not os.path.exists(output_hist_dir):
    os.makedirs(output_hist_dir)

filelist = os.listdir(base_dir)
filelist.sort(key=lambda x: int(x.split('.')[0]))
i = 1

for i in range(0, len(filelist)):
    path = os.path.join(base_dir, filelist[i])
    save_path2 = out_gray_dir + str(i+1) + 'gray.jpg'
    save_path3 = output_erzhihua_dir + str(i + 1) + 'erzhihua.jpg'
    save_path4 = output_otsu_dir + str(i+1) + 'otsu.jpg'
    save_path5 = output_hist_dir + str(i+1) + 'hist.jpg'
    save_path6 = output_mean_dir + str(i+1) + 'mean.jpg'

    img0 = cv2.imread(path, cv2.IMREAD_COLOR)  # 读取格式为BGR
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)  # 转换为RGB
    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # 转换为灰度图
    cv2.imwrite(save_path2, gray)

    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # 转换为灰度图
    ret1, mask = cv2.threshold(gray, 230, 255, 0)  # 简单二值化
    cv2.imwrite(save_path3, mask)

    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # 转换为灰度图
    ret2, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # otsu法二值化
    cv2.imwrite(save_path4, threshold)

    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # 转换为灰度图
    hist_binary = hist_binarization(gray) #双峰法二值化
    cv2.imwrite(save_path5, hist_binary)

    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # 转换为灰度图
    mean_binary = mean_binarization(gray) #平均值二值化
    cv2.imwrite(save_path6, mean_binary)

    print( i+1 )
