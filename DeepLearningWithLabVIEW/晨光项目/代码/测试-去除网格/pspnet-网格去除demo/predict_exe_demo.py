# 2023.3.27  @yaofanghao
# 实现输入单张图片--分块--模型预测--拼接--输出完整图片--霍夫线检测算法--输出图与原图叠加去除网格--保存至指定路径功能
# 并打包成exe
# ---------------------------
# 程序命令行输入方式示例：
#       输入：
#           test.jpg
#       输出：
#           test_img_block/
#           test_img_out/
#           test_img_out/test_final_out.jpg

# import sys
import cv2
import numpy as np
from PIL import Image
import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # 忽略TensorFlow的warning信息
import tensorflow as tf
from tqdm import tqdm
import matplotlib.pyplot as plt
from pspnet import Pspnet
import datetime

# 使用GPU,
# 但在程序刚开始加载 Successfully opened dynamic library cudart64_110.dll 后会卡顿
# gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)

# 使用CPU，
# 速度也可以接受
os.environ["CUDA_VISIBLE_DEVICES"] ="-1"

# 图像分块 分成m行n列    
def divide_method2(img, m, n):
    h, w = img.shape[0], img.shape[1]
    grid_h = int(h * 1.0 / (m - 1) + 0.5)  # 每个网格的高
    grid_w = int(w * 1.0 / (n - 1) + 0.5)  # 每个网格的宽

    # 满足整除关系时的高、宽
    h = grid_h * (m - 1)
    w = grid_w * (n - 1)

    # 图像缩放
    img_re = cv2.resize(img, (w, h),cv2.INTER_LINEAR)
    gx, gy = np.meshgrid(np.linspace(0, w, n), np.linspace(0, h, m))
    gx = gx.astype(np.int)
    gy = gy.astype(np.int)

    # 这是一个五维的张量，前面两维表示分块后图像的位置（第m行，第n列），后面三维表示每个分块后的图像信息
    divide_image = np.zeros([m - 1, n - 1, grid_h, grid_w, 3],
                            np.uint8)
    for i in range(m - 1):
        for j in range(n - 1):
            divide_image[i, j, ...] = img_re[
                                      gy[i][j]:gy[i + 1][j + 1], gx[i][j]:gx[i + 1][j + 1], :]
    return divide_image

# 保存图片
def display_blocks(divide_image):
    m, n = divide_image.shape[0], divide_image.shape[1]
    num = 1
    for i in range(m):
        for j in range(n):
            plt.imsave("{}/{}.jpg".format(dir_origin_path,num), divide_image[i, j, :])
            # print("processing..." + str(num))
            num += 1
    plt.show()

if __name__ == "__main__":

    time1 = datetime.datetime.now()
    # ------------------参数设置区域
    pspnet = Pspnet()
    # if len(sys.argv) ==1:
    #     print("start: python predict_exe_demo.py test.jpg 2 10")
    #     img_name = "test.jpg"
    #     m = 2  # 图像分块的行数
    #     n = 10  # 图像分块的列数
    # else:  # 传入图片名称参数
    #     img_name = sys.argv[1]
    #     m = int(sys.argv[2])
    #     n = int(sys.argv[3])
    # if (m<=1) | (n<=1):
    #     raise AssertionError("Invalid input of m or n, m and n must bigger than 1.")

    img_name = input("Input image filename:")
    try:
        image = Image.open(img_name)
    except:
        raise AssertionError('Fail to open image!')
    m = 2
    n = 10

    filename, _ = os.path.splitext(img_name)
    name_classes = ["background","grid"]
    dir_origin_path = str(filename) + '_img_block/'
    dir_save_path = str(filename) + "_img_out/"
    output_save_path = str(dir_save_path) + "final_out.jpg"
    if not os.path.exists(dir_origin_path):
        os.makedirs(dir_origin_path)
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)

    # ------------------图像分块
    img = cv2.imdecode(np.fromfile(img_name, dtype=np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print("start divide image... / m (row) is 2, n (column) is 10.")
    divide_image2 = divide_method2(img, m+1, n+1)  # 该函数中m+1和n+1表示网格点个数，m和n分别表示分块的块数
    display_blocks(divide_image2)
    print("divide image success!")

    # ------------------图像导入模型预测
    # 原分块图像文件夹路径为 dir_origin_path
    # 模型预测结果图像保存至 dir_save_path
    img_names = os.listdir(dir_origin_path)
    img_names.sort(key=lambda x: int(x[:-4]))
    # 读取分块后图片的长宽 用于后续拼接
    img_test_path = str(dir_origin_path) + str(img_names[0])
    img_test = cv2.imdecode(np.fromfile(img_test_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    h, w = img_test.shape[0], img_test.shape[1]
    print("start dir_predict image...")
    for _img_name in tqdm(img_names):
        if _img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            image_path  = os.path.join(dir_origin_path, _img_name)
            image       = Image.open(image_path)
            r_image     = pspnet.detect_image(image)
            if not os.path.exists(dir_save_path):
                os.makedirs(dir_save_path)
            r_image.save(os.path.join(dir_save_path, _img_name))
    print("dir_predict image success!")

    # ------------------图像拼接
    # 保存整张图像至output_save_path
    # image_save_names = [name for name in os.listdir(dir_save_path) for item in dir_save_path if
    #             os.path.splitext(name)[1] == item]
    image_save_names = os.listdir(dir_save_path)
    image_save_names.sort(key=lambda x: int(x[:-4]))
    if len(image_save_names) != m * n:
        raise ValueError("row*colum != num!")
    to_image = Image.new('L',(n*w, m*h),'white' )  # 创建一个新图 L模式表示灰度图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    print("start compose image...")
    for y in range(1, m+1):
        for x in range(1, n+1):
            from_image = Image.open(dir_save_path + image_save_names[n*(y-1)+x-1]).resize((w, h), 
                            Image.ANTIALIAS)
            to_image.paste(from_image, ((x-1)*w, (y-1)*h))
    to_image_array = np.array(to_image)
    print("compose image success!")

    # ------------------输出图与原图叠加去除网格
    src0 = cv2.imdecode(np.fromfile(img_name, dtype=np.uint8), cv2.IMREAD_COLOR)
    src = np.copy(src0)

    # Probabilistic Line Transform
    # 累计概率霍夫变换算法
    dst = cv2.Canny(src0, 0, 150, None, 3)
    cdstP = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    # 用法：(image, rho, theta, threshold,
    #           lines=None, minLineLength=None, maxLineGap=None)
    linesP = cv2.HoughLinesP(dst, 2, np.pi / 180, 150,
                            None, minLineLength=1, maxLineGap=1)
    # 画霍夫变换检测到的线（红色）
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 5, cv2.LINE_AA)

    print("start mix image...")
    # 选取src和to_image_array两者的最小尺寸做遍历
    _i = min(src.shape[0], to_image_array.shape[0])
    _j = min(src.shape[1], to_image_array.shape[1])
    for i in tqdm(range(_i)):
        for j in range(_j):
            if (to_image_array[i,j]>250):
                src[i,j] = 255  # 对深度学习预测得到的图片中的白色部分排除为缺陷的可能，设置为白色
            if (cdstP[i, j][0] == 0) & (cdstP[i, j][1] == 0) & (cdstP[i, j][2] == 255):
                src[i, j] = 255  # # 对霍夫P线检测中的红色部分排除为缺陷的可能，设置为白色
            else:
                pass
    mix = cv2.add(src0, src)
    cv2.imencode('.jpg', mix)[1].tofile(output_save_path)  # 保存图片，解决了中文路径报错的问题
    print("mix image success!")

    time2 = datetime.datetime.now()
    print("total time:", str(time2-time1))