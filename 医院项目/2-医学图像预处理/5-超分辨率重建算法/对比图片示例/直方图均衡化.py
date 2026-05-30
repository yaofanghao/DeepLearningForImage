# 2023.2.14 批量对图片进行直方图均衡化，目的是增强训练集的纹理特征
import numpy as np
import cv2 as cv
import os

# 彩色图像进行自适应直方图均衡化
def hisEqulColor(img):
    ## 将RGB图像转换到YCrCb空间中
    ycrcb = cv.cvtColor(img, cv.COLOR_BGR2YCR_CB)
    # 将YCrCb图像通道分离
    channels = cv.split(ycrcb)
    # 参考来源： https://docs.opencv.org/4.1.0/d5/daf/tutorial_py_histogram_equalization.html
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe.apply(channels[0], channels[0])
    cv.merge(channels, ycrcb)
    cv.cvtColor(ycrcb, cv.COLOR_YCR_CB2BGR, img)
    return img

################ 修改内容区域
DATADIR = "E:\\MyGithub\\11\\3"  # 原图片路径
save_dir = "E:\\MyGithub\\11\\3-output\\"  # 处理后图片路径
#######################

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
path = os.path.join(DATADIR)
img_list = os.listdir(path)

# 按顺序读取图片
# img_list.sort(key=lambda x: int(x[:-4]))
ind = 0
for i in img_list:
    pathjpg = os.path.join(path, i)
    print(i)
    filename, extension = os.path.splitext(i)
    img = cv.imdecode(np.fromfile(pathjpg, dtype=np.uint8), cv.IMREAD_COLOR)

    res = hisEqulColor(img)

    ind = ind + 1
    save_path = save_dir + str(filename) + '.jpg'
    cv.imencode('.jpg', res)[1].tofile(save_path)  # 保存图片，解决了中文路径报错的问题