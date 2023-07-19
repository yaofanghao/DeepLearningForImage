# 2023.2.14 批量对图片进行直方图均衡化，目的是增强训练集的纹理特征
# 2023.7.19 针对软管项目，继续做了一点改进
import numpy as np
import cv2 as cv
import os


################ 修改内容区域
DATADIR = "before"  # 原图片路径
save_dir = "output\\"  # 处理后图片路径
#######################

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
path = os.path.join(DATADIR)
img_list = os.listdir(path)


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


# 亮度增强
def data_augment_demo(image, brightness):
    # factor = 1.0 + random.uniform(-1.0*brightness, brightness)
    factor = 1.0+brightness
    table = np.array([(i / 255.0) * factor * 255 for i in np.arange(0, 256)]).clip(0,255).astype(np.uint8)
    image = cv.LUT(image, table)
    return image, factor


# 对白色区域覆盖为另一种暗色
def convert_white(image):
    # 将图像从BGR色彩空间转换为灰度图像
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # 使用固定阈值来分割图像，将灰度值大于阈值的像素设为255（白色），小于等于阈值的像素设为0（黑色）
    _, binary_image = cv.threshold(gray_image, 254, 255, cv.THRESH_BINARY)

    # 创建目标颜色
    target_color = (128, 128, 128)

    # 将二值化图像中的白色部分替换为目标颜色
    result = image.copy()
    result[binary_image == 255] = target_color

    return result


# 按顺序读取图片
# img_list.sort(key=lambda x: int(x[:-4]))
ind = 0
for i in img_list:
    pathjpg = os.path.join(path, i)
    print(i)
    filename, extension = os.path.splitext(i)
    img = cv.imdecode(np.fromfile(pathjpg, dtype=np.uint8), cv.IMREAD_COLOR)

    # 图像处理模块
    res = hisEqulColor(img)
    res, factor = data_augment_demo(res, 0.5)
    res = convert_white(res)

    # 保存图片，解决了中文路径报错的问题
    ind = ind + 1
    save_path = save_dir + str(filename) + '.jpg'
    cv.imencode('.jpg', res)[1].tofile(save_path)