import cv2
import os

base_dir = "./jpg"  # 要二值化的图片的原文件夹位置
output_dir = './erzhihua/'  # 二值化处理后存放的文件夹位置

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
filelist = os.listdir(base_dir)
filelist.sort(key=lambda x: int(x.split('.')[0]))
i = 1

for i in range(0, len(filelist)):
    path = os.path.join(base_dir, filelist[i])
    # print(path)
    img0 = cv2.imread(path, cv2.IMREAD_COLOR)  # 读取格式为BGR
    img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)  # 转换为RGB
    gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # 转换为灰度图
    ret, mask = cv2.threshold(gray, 230, 255, 0) #简单二值化
    save_path = output_dir + str(i+1) + '.jpg'  #保存至另一文件夹
    cv2.imwrite(save_path, mask)
    print( i+1 )
