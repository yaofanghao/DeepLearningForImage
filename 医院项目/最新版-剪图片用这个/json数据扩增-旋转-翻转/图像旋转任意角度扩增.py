from PIL import Image
import numpy as np
import os

# 图像旋转任意角度的简单实现
# 2022.12.1 更新至最新版本。实现全自动扩增，完成了封装，增加可移植性
#######################
# 修改内容区域：
rotate_angle = 175  # 旋转角度
jpg_dir = './JPEGImages'  # 原图文件夹
png_dir = './SegmentationClass' # 原标注png文件夹
#######################

jpg_save_dir = './JPEGImages_rot' + str(rotate_angle) #扩增后图片的文件夹
png_save_dir = './SegmentationClass_rot' + str(rotate_angle) #扩增后标注png的文件夹
if not os.path.exists(jpg_save_dir):
    os.makedirs(jpg_save_dir)
if not os.path.exists(png_save_dir):
    os.makedirs(png_save_dir)

# 图像扩增四倍的函数
def img_rot(input_dir, output_dir, rotate_angle):
    alist = os.listdir(input_dir)
    for i in range(0, len(alist)):
        path = os.path.join(input_dir, alist[i])
        AnnotFilePath = path

        # 原图
        img = np.asarray(Image.open(AnnotFilePath))
        _, AnnotFileName = os.path.split(AnnotFilePath)
        image, image_format = AnnotFileName.split('.')
        NewPath = os.path.join(output_dir, image + str('.') + image_format)
        Image.fromarray(img).save(NewPath)
        print("保存原图至" + str(NewPath))

        # 旋转指定角度后
        img = Image.open(AnnotFilePath)
        img = img.rotate(rotate_angle)
        _, AnnotFileName = os.path.split(AnnotFilePath)
        image, image_format = AnnotFileName.split('.')
        NewPath = os.path.join(output_dir, image + str('_') + str(rotate_angle)
                               + str('.') + image_format)
        # Image.fromarray(img).save(NewPath)
        img.save(NewPath)
        print("保存旋转"+str(rotate_angle)+"角度的图片至" + str(NewPath))
        print("统计：" + str(i+1))
        print("-----------------")


if __name__ == '__main__':

    # 分别对jpg和png图片旋转rotate_angle的角度
    img_rot(jpg_dir, jpg_save_dir, rotate_angle)
    img_rot(png_dir, png_save_dir, rotate_angle)
    print("扩增完成")
