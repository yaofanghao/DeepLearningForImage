from PIL import Image
import numpy as np
import os

# 图像扩增四倍的简单实现
# 2022.12.1 更新至最新版本。实现全自动扩增，完成了封装，增加可移植性
#######################
# 修改内容区域：
jpg_dir='./JPEGImages'  # 原图文件夹
jpg_save_dir = './JPEGImages_aug'  #扩增后图片的文件夹
png_dir='./SegmentationClass'  # 原标注png文件夹
png_save_dir = './SegmentationClass_aug'  #扩增后标注png的文件夹
#######################
if not os.path.exists(jpg_save_dir):
    os.makedirs(jpg_save_dir)
if not os.path.exists(png_save_dir):
    os.makedirs(png_save_dir)

# 图像扩增四倍的函数
def img_aug(input_dir, output_dir):
    alist = os.listdir(input_dir)
    for i in range(0, len(alist)):
        path = os.path.join(input_dir, alist[i])
        AnnotFilePath = path

        # 原图理解为第一象限
        img = np.asarray(Image.open(AnnotFilePath))
        _, AnnotFileName = os.path.split(AnnotFilePath)
        image, image_format = AnnotFileName.split('.')
        NewPath = os.path.join(output_dir, image + str('.') + image_format)
        Image.fromarray(img).save(NewPath)
        print("保存原图至" + str(NewPath))

        # 左右翻转 第二象限
        img = np.asarray(Image.open(AnnotFilePath))
        img1 = np.fliplr(img)
        _, AnnotFileName = os.path.split(AnnotFilePath)
        image, image_format = AnnotFileName.split('.')
        NewPath = os.path.join(output_dir, image + str('_1.') + image_format)
        Image.fromarray(img1).save(NewPath)
        print("保存左右翻转图至" + str(NewPath))

        # 上下翻转 第四象限
        img = np.asarray(Image.open(AnnotFilePath))
        img2 = np.flip(img, 0)
        _, AnnotFileName = os.path.split(AnnotFilePath)
        image, image_format = AnnotFileName.split('.')
        NewPath = os.path.join(output_dir, image + str('_2.') + image_format)
        Image.fromarray(img2).save(NewPath)
        print("保存上下翻转图至" + str(NewPath))

        # 左右并上下翻转 第三象限
        img = np.asarray(Image.open(AnnotFilePath))
        img3 = np.fliplr(img)
        img4 = np.flip(img3, 0)
        _, AnnotFileName = os.path.split(AnnotFilePath)
        image, image_format = AnnotFileName.split('.')
        NewPath = os.path.join(output_dir, image + str('_3.') + image_format)
        Image.fromarray(img4).save(NewPath)
        print("保存左右并上下翻转图至" + str(NewPath))
        print("统计：" + str(i+1))
        print("-----------------")

if __name__ == '__main__':

    # 分别对jpg和png图片扩增
    img_aug(jpg_dir, jpg_save_dir)
    img_aug(png_dir, png_save_dir)
    print("扩增完成")
