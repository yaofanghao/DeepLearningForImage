# 2023.2.16- 综合评估代码修改中 @yaofanghao

import numpy
from PIL import Image
import os
from frcnn import FRCNN

if __name__ == "__main__":
    frcnn = FRCNN()

    dir_weidou_path = "weidou/"
    dir_weiti_path = "weiti/"
    dir_save_path = "img_out"

################# 修改中。。。。。2023.2.17
    all_save_path_0 = str(dir_save_path) + "_0-1/"
    all_save_path_2 = str(dir_save_path) + "_2/"
    all_save_path_high = str(dir_save_path) + "_high/"
    all_save_path_none = str(dir_save_path) + "_none/"
    if not os.path.exists(all_save_path_0):
        os.makedirs(all_save_path_0)
    if not os.path.exists(all_save_path_2):
        os.makedirs(all_save_path_2)
    if not os.path.exists(all_save_path_high):
        os.makedirs(all_save_path_high)
    if not os.path.exists(all_save_path_none):
        os.makedirs(all_save_path_none)

    ############  预测胃窦文件夹中所有图片
    img_names = os.listdir(dir_weidou_path)
    # img_names.sort(key=lambda x:int(x.split('.')[0]))  # 按照1，2，3顺序读图片
    for img_name in img_names:
        image_path = os.path.join(dir_weidou_path, img_name)
        image = Image.open(image_path)

        # 修改detect_image 的返回值
        r_image, out_scores, out_classes,top,right, left,bottom= frcnn.detect_image(image)

        filename, extension = os.path.splitext(img_name)

        out_scores_size = out_scores.size
        # print(out_scores)
        # print(out_classes)
        test1 = out_classes
        test1 = numpy.asarray(test1, dtype=int)
        out_scores = numpy.around(out_scores,3)
        # print(out_scores.max()) # 这句不能有，会报错

        if out_scores.size != 0:
            ################ 找到置信度最大的类别的算法 ############
            num = 0
            t = out_scores
            class0 = numpy.array([0])
            class2 = numpy.array([0])
            class3 = numpy.array([0])
            for i in out_classes:
                if i == 0:
                    class0 = numpy.append(class0, t[num])
                if i == 1:
                    class2 = numpy.append(class2, t[num])
                if i == 2:
                    class3 = numpy.append(class3, t[num])
                num += 1
            class0_max = numpy.max(class0)
            class0_max=round(class0_max, 4)
            class2_max = numpy.max(class2)
            class2_max=round(class2_max, 4)
            class3_max = numpy.max(class3)
            class3_max=round(class3_max, 4)
            locat = out_scores.argmax(axis=None, out=None)  # 预测结果最大值的位置
            out_scores_max = out_scores.max()  # 预测结果最大值
            out_scores_max =round(out_scores_max,4)   # 小数点后4位
            a = out_classes
            class_max_confidence = a[locat]  # 预测结果最大值的位置的类别
            # print(class_max_confidence)

            if class_max_confidence == 0:
                class_max_confidence = '0-1'
                r_image.save(os.path.join(all_save_path_0, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
            if class_max_confidence == 1:
                class_max_confidence = '2'
                r_image.save(os.path.join(all_save_path_2, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)
            if class_max_confidence == 2:
                class_max_confidence = '3'
                r_image.save(os.path.join(all_save_path_high, img_name.replace(".jpg", ".png")),quality=95, subsampling=0)

        else: # 没有识别出任何一个框
            r_image.save(os.path.join(all_save_path_none, img_name.replace(".jpg", ".png")), quality=95,subsampling=0)

        print("图片名为：")
        print(img_name)
        print(class_max_confidence)
    ############  预测胃体文件夹中所有图片

    ############  综合评估结果，输出 0-1 / 2 / high risk ，并将图片全部保存至对应文件夹