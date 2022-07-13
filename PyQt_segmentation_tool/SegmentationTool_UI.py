"""
  语义分割训练前处理工具
  主要功能：
           FUNC1：视频素材转换成图像
           FUNC2：把标注后json文件和对应的jpg文件从混合的文件夹中提取出来
           FUNC3：Json_to_Dataset功能.从Json文件获得标签文件
           FUNC4：Get_JPG_PNG从上一步的Dataset文件中提取训练图像和训练标签
           FUNC5：从训练集中随机选取一定比例的图像和标签作为验证集图像和标签
           FUNC6：由模型输出标签和人工标签计算得到MIOU和MPA
  BY LiangBo
"""

import sys
import numpy as np
import os, random, shutil
from SegmentationTool import Ui_MainWindow
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import cv2
from PyQt5.QtCore import QTimer, QCoreApplication
from PIL import Image
import argparse
import json
import os.path as osp
import warnings
import PIL.Image
import yaml
from labelme import utils
import draw
import base64

__all__ = ['SegmentationMetric']


class Seg_Tool(QMainWindow, Ui_MainWindow):
    # 初始化
    def __init__(self, parent=None):
        super(Seg_Tool, self).__init__(parent)
        self.setupUi(self)
        self.CallBack()
        # 语义分割类选择，有几类就改为几
        self.numClass = 2  
        self.confusionMatrix = np.zeros((self.numClass,) * 2)

    # 按键关联回调函数
    def CallBack(self):
        self.sel_video_file.clicked.connect(self.OpenVideo)
        self.sel_savepic_file.clicked.connect(self.SelectSavePlace)
        self.video_pic_change.clicked.connect(self.Start_Videopic_Change)
        self.sel_jsonjpg_file.clicked.connect(self.SelectJsonjpgPlace)
        self.sel_jsonsave_file.clicked.connect(self.SelectJsonsavePlace)
        self.sel_jpgsave_file.clicked.connect(self.SelectJpgsavePlace)
        self.json_jpg_change.clicked.connect(self.Jsonjpg_Change)
        self.sel_trainimage_file.clicked.connect(self.Select_train_image)
        self.sel_trainlabel_file.clicked.connect(self.Select_train_label)
        self.sel_valimage_file.clicked.connect(self.Select_val_image)
        self.sel_vallabel_file.clicked.connect(self.Select_val_label)
        self.train_val_change.clicked.connect(self.Train_Val_Change)
        self.sel_model_label.clicked.connect(self.Model_label)
        self.sel_handle_label.clicked.connect(self.Handle_label)
        self.sel_Jsonjpg.clicked.connect(self.select_Jsonjpg)
        self.sel_output.clicked.connect(self.select_output)
        self.Do_jsontodataset.clicked.connect(self.Json_to_dataset)
        self.compute_iou.clicked.connect(self.Compute)
        self.sel_Jsonjpg_2.clicked.connect(self.select_Jsonjpg_2)
        self.sel_Output_file.clicked.connect(self.select_out2)
        self.sel_Classname_file.clicked.connect(self.select_classname)
        self.sel_JPG_file.clicked.connect(self.select_jpg2)
        self.sel_PNG_file.clicked.connect(self.select_png2)
        self.do_get_jpgpng.clicked.connect(self.Get_jpg_png)
        self.exit_button.clicked.connect(self.exitApp)
    
    # <--------------FUNC1：视频素材转换成图像------------------>
    # 视频转图像视频文件读入
    def PrepCamera(self):
        try:
            self.camera = cv2.VideoCapture(self.video_pic_path[0])
        except:
            self.lineEdit_videopic_change.setText("Video Loading Error!!!")

    def OpenVideo(self):
        self.video_pic_path = QFileDialog.getOpenFileName(self, '选择要转换的视频文件', './', "(*.mp4)")
        self.lineEdit_video.setText(self.video_pic_path[0])
        self.PrepCamera()

    # 选择图像存储位置
    def SelectSavePlace(self):
        dirname = QFileDialog.getExistingDirectory(self, "选择图像存储文件夹", '.')
        if dirname:
            self.lineEdit_image.setText(dirname)
            self.SavePathChange = dirname + '/'

    # 视频转图像函数
    def Start_Videopic_Change(self):
        total_frame_number = self.camera.get(cv2.CAP_PROP_FRAME_COUNT)
        image_index = 1
        while (image_index - 1) < total_frame_number:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.resize(frame , (640,320))
                filename = str(image_index) + '.jpg'
                cv2.imwrite(self.SavePathChange + filename, frame)
                image_index += 1
            elif frame is None:
                self.lineEdit_videopic_change.setText("Write process is at the end.\n")
            else:
                self.lineEdit_videopic_change.setText("Cannot process the image ", str(image_index),
                                                      "! Write to the image failed! \n")
        self.lineEdit_videopic_change.setText("Change Finish!!!")

    # 选择Json和jpg共同存在的文件夹
    def SelectJsonjpgPlace(self):
        dirname1 = QFileDialog.getExistingDirectory(self, "选择Json/Jpg素材文件夹", '.')
        if dirname1:
            self.lineEdit_jsonjpg.setText(dirname1)
            self.SaveJsonjpgChange = dirname1 + '/'

    # 选择json文件存放的位置
    def SelectJsonsavePlace(self):
        dirname2 = QFileDialog.getExistingDirectory(self, "选择Json存放文件夹", '.')
        if dirname2:
            self.lineEdit_json.setText(dirname2)
            self.SaveJsonChange = dirname2 + '/'

    # 选择jpg文件存放的位置
    def SelectJpgsavePlace(self):
        dirname3 = QFileDialog.getExistingDirectory(self, "选择Jpg存放文件夹", '.')
        if dirname3:
            self.lineEdit_jpg.setText(dirname3)
            self.SaveJpgChange = dirname3 + '/'

    # json-jpg------>json
    #           |___>jpg
    def Jsonjpg_Change(self):
        self.write_file_name = self.SaveJsonjpgChange + '/dir.txt'
        self.extract_name(self.SaveJsonjpgChange, self.write_file_name)
        self.moveJPG(self.SaveJsonjpgChange, self.write_file_name)
        self.moveJSON(self.SaveJsonjpgChange, self.write_file_name)
        self.lineEdit_jsonjpg_change.setText('Move Finish!!!')

    def extract_name(self, Image_dir, write_file_name):
        file_list = []                           # 读取文件，并将地址、图片名和标签写到txt文件中
        write_file = open(write_file_name, "w")  # 打开write_file_name文件
        for file in os.listdir(Image_dir):
            if file.endswith(".json"):
                name = file.split('.')[0]        # JSON名称和后缀名
                write_name = name
                file_list.append(write_name)
        sorted(file_list)                        # 将列表中所有元素随机排列
        number_of_lines = len(file_list)
        for current_line in range(number_of_lines):
            write_file.write(file_list[current_line] + '\n')
        write_file.close()

    def moveJPG(self, fileLabelDir, write_file_name):
        pathDir = os.listdir(fileLabelDir)
        f = open(write_file_name, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')               # 去除文本的换行符，否则报错
            shutil.move(fileLabelDir + str(line) + '.jpg', self.SaveJpgChange + str(line) + '.jpg')

    def moveJSON(self, fileLabelDir, write_file_name):
        pathDir = os.listdir(fileLabelDir)
        f = open(write_file_name, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')               # 去除文本的换行符，否则报错
            shutil.move(fileLabelDir + str(line) + '.json', self.SaveJsonChange + str(line) + '.json')

    # <-------------FUNC5：从训练集中随机选取一定比例的图像和标签作为验证集图像和标签---------------->
    def Select_train_image(self):
        dirname4 = QFileDialog.getExistingDirectory(self, "选择训练集图像文件夹", '.')
        if dirname4:
            self.lineEdit_trainimage.setText(dirname4)
            self.SaveTrainimageChange = dirname4 + '/'

    def Select_train_label(self):
        dirname5 = QFileDialog.getExistingDirectory(self, "选择训练集标签文件夹", '.')
        if dirname5:
            self.lineEdit_trainlabel.setText(dirname5)
            self.SaveTrainlabelChange = dirname5 + '/'

    def Select_val_image(self):
        dirname6 = QFileDialog.getExistingDirectory(self, "选择验证集图像文件夹", '.')
        if dirname6:
            self.lineEdit_valimage.setText(dirname6)
            self.SaveValimageChange = dirname6 + '/'

    def Select_val_label(self):
        dirname7 = QFileDialog.getExistingDirectory(self, "选择验证集标签文件夹", '.')
        if dirname7:
            self.lineEdit_vallabel.setText(dirname7)
            self.SaveVallabelChange = dirname7 + '/'

    def Train_Val_Change(self):
        self.write_file_name_random = self.SaveValimageChange + '/dir.txt'
        self.moveImage(self.SaveTrainimageChange)
        self.extract_name_random(self.SaveValimageChange, self.write_file_name_random)
        self.moveLabel(self.SaveTrainlabelChange, self.write_file_name_random)
        self.lineEdit_trainval_change.setText('Random Move Finish!!!')

    def moveImage(self, fileImageDir):
        pathDir = os.listdir(fileImageDir)
        filenumber = len(pathDir)
        rate = float(self.lineEdit_valtrain.text())
        picknumber = int(filenumber * rate)  # 按照设定比例从文件夹中取一定数量图片
        sample = random.sample(pathDir, picknumber)
        print(sample)
        for name in sample:
            shutil.move(fileImageDir + name, self.SaveValimageChange + name)
        return

    def extract_name_random(self, Image_dir, write_file_name):
        file_list = []
        # 读取文件，并将地址、图片名和标签写到txt文件中
        write_file = open(write_file_name, "w")     # 打开write_file_name文件
        for file in os.listdir(Image_dir):
            if file.endswith(".jpg"):
                name = file.split('.')[0]           # 分割图像名称和后缀名
                write_name = name
                file_list.append(write_name)
        sorted(file_list)                           # 将列表中所有元素随机排列
        number_of_lines = len(file_list)
        for current_line in range(number_of_lines):
            write_file.write(file_list[current_line] + '\n')
        write_file.close()

    def moveLabel(self, fileLabelDir, write_file_name):
        pathDir = os.listdir(fileLabelDir)
        f = open(write_file_name, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')                 # 去除文本的换行符，否则报错
            shutil.move(fileLabelDir + str(line) + '.png', self.SaveVallabelChange + str(line) + '.png')

    # <-------------FUNC6：由模型输出标签和人工标签计算得到MIOU和MPA---------------->
    def Model_label(self):
        dirname8 = QFileDialog.getExistingDirectory(self, "选择模型输出标签文件夹", '.')
        if dirname8:
            self.lineEdit_modellabel.setText(dirname8)
            self.ModellabelChange = dirname8 + '/'

    def Handle_label(self):
        dirname9 = QFileDialog.getExistingDirectory(self, "选择手工标注标签文件夹", '.')
        if dirname9:
            self.lineEdit_handlelabel.setText(dirname9)
            self.HandlelabelChange = dirname9 + '/'

    def pixelAccuracy(self):
        # return all class overall pixel accuracy
        #  PA = acc = (TP + TN) / (TP + TN + FP + TN)
        acc = np.diag(self.confusionMatrix).sum() / self.confusionMatrix.sum()
        return acc

    def classPixelAccuracy(self):
        # return each category pixel accuracy(A more accurate way to call it precision)
        # acc = (TP) / TP + FP
        classAcc = np.diag(self.confusionMatrix) / self.confusionMatrix.sum(axis=1)
        return classAcc                 # 返回的是一个列表值，如：[0.90, 0.80, 0.96]，表示类别1 2 3各类别的预测准确率

    def meanPixelAccuracy(self):
        classAcc = self.classPixelAccuracy()
        meanAcc = np.nanmean(classAcc)  # np.nanmean 求平均值，nan表示遇到Nan类型，其值取为0
        return meanAcc                  # 返回单个值，如：np.nanmean([0.90, 0.80, 0.96, nan, nan]) = (0.90 + 0.80 + 0.96） / 3 =  0.89

    def meanIntersectionOverUnion(self):
        # Intersection = TP Union = TP + FP + FN
        # IoU = TP / (TP + FP + FN)
        intersection = np.diag(self.confusionMatrix)    # 取对角元素的值，返回列表
        union = np.sum(self.confusionMatrix, axis=1) + np.sum(self.confusionMatrix, axis=0) - np.diag(
            self.confusionMatrix)                       # axis = 1表示混淆矩阵行的值，返回列表； axis = 0表示取混淆矩阵列的值，返回列表
        IoU = intersection / union                      # 返回列表，其值为各个类别的IoU
        mIoU = np.nanmean(IoU)                          # 求各类别IoU的平均
        return mIoU

    def genConfusionMatrix(self, imgPredict, imgLabel):  # 同FCN中score.py的fast_hist()函数
        # remove classes from unlabeled pixels in gt image and predict
        mask = (imgLabel >= 0) & (imgLabel < self.numClass)
        label = self.numClass * imgLabel[mask] + imgPredict[mask]
        count = np.bincount(label, minlength=self.numClass ** 2)
        confusionMatrix = count.reshape(self.numClass, self.numClass)
        return confusionMatrix

    def Frequency_Weighted_Intersection_over_Union(self):
        # FWIOU =     [(TP+FN)/(TP+FP+TN+FN)] *[TP / (TP + FP + FN)]
        freq = np.sum(self.confusion_matrix, axis=1) / np.sum(self.confusion_matrix)
        iu = np.diag(self.confusion_matrix) / (
            np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
            np.diag(self.confusion_matrix))
        FWIoU = (freq[freq > 0] * iu[freq > 0]).sum()
        return FWIoU

    def addBatch(self, imgPredict, imgLabel):
        assert imgPredict.shape == imgLabel.shape
        self.confusionMatrix += self.genConfusionMatrix(imgPredict, imgLabel)

    def reset(self):
        self.confusionMatrix = np.zeros((self.numClass, self.numClass))

    def extract_name_label(self, Image_dir, write_file_name):
        file_list = []
        # 读取文件，并将地址、图片名和标签写到txt文件中
        write_file = open(write_file_name, "w")  # 打开write_file_name文件
        for file in os.listdir(Image_dir):
            if file.endswith(".png"):
                name = file.split('.')[0]        # 分割图像名称和后缀名
                write_name = name
                file_list.append(write_name)
        sorted(file_list)                        # 将列表中所有元素随机排列
        number_of_lines = len(file_list)
        for current_line in range(number_of_lines):
            write_file.write(file_list[current_line] + '\n')
        write_file.close()

    def Compute(self):
        path1 = self.ModellabelChange
        path2 = self.HandlelabelChange
        self.write_file_name_label = path1 + '/dir.txt'
        self.extract_name_label(path1, self.write_file_name_label)
        cnt = 0
        iou = []
        Mpa = []
        f = open(self.write_file_name_label, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')  # 去除文本的换行符，否则报错
            img = cv2.imread(path1 + str(line) + '.png')
            label = cv2.imread(path2 + str(line) + '.png')
            imgPredict = np.array(img)
            imgLabel = np.array(label)
            self.addBatch(imgPredict, imgLabel)
            pa = self.pixelAccuracy()
            cpa = self.classPixelAccuracy()
            mpa = self.meanPixelAccuracy()
            mIoU = self.meanIntersectionOverUnion()
            # print('pa is : %f' % pa)
            # print('cpa is :') # 列表
            # print(cpa)
            # print('mpa is : %f' % mpa)
            # print('mIoU is : %f' % mIoU)
            Mpa.append(mpa)
            iou.append(mIoU)
            cnt += 1
        average_iou = np.mean(iou)
        average_pa = np.mean(Mpa)
        self.textEdit_iou.setPlainText("平均MIOU：" + str(average_iou) + '\r\n'
                                       + '平均MPA：' + str(average_pa))

    ##################FUNC3：Json_to_Dataset功能#####################
    def select_Jsonjpg(self):
        dirname10 = QFileDialog.getExistingDirectory(self, "选择存放Json和Jpg文件的文件夹", '.')
        if dirname10:
            self.lineEdit_Jsonjpg.setText(dirname10)
            self.JsonjpgChange = dirname10 + '/'
            self.Jsonjpg7 = dirname10

    def select_output(self):
        dirname11 = QFileDialog.getExistingDirectory(self, "选择一个存放输出文件夹", '.')
        if dirname11:
            self.lineEdit_output.setText(dirname11)
            self.outputChange = dirname11 + '/'

    def Json_to_dataset(self):
        count = os.listdir(self.JsonjpgChange)
        for i in range(0, len(count)):
            path = os.path.join(self.Jsonjpg7, count[i])

            if os.path.isfile(path) and path.endswith('json'):
                data = json.load(open(path))

                if data['imageData']:
                    imageData = data['imageData']
                else:
                    imagePath = os.path.join(os.path.dirname(path), data['imagePath'])
                    with open(imagePath, 'rb') as f:
                        imageData = f.read()
                        imageData = base64.b64encode(imageData).decode('utf-8')
                img = utils.img_b64_to_arr(imageData)
                label_name_to_value = {'_background_': 0}
                for shape in data['shapes']:
                    label_name = shape['label']
                    if label_name in label_name_to_value:
                        label_value = label_name_to_value[label_name]
                    else:
                        label_value = len(label_name_to_value)
                        label_name_to_value[label_name] = label_value

                # label_values must be dense
                label_values, label_names = [], []
                for ln, lv in sorted(label_name_to_value.items(), key=lambda x: x[1]):
                    label_values.append(lv)
                    label_names.append(ln)
                assert label_values == list(range(len(label_values)))

                lbl = utils.shapes_to_label(img.shape, data['shapes'], label_name_to_value)

                captions = ['{}: {}'.format(lv, ln)
                            for ln, lv in label_name_to_value.items()]
                lbl_viz = draw.draw_label(lbl, img, captions)
                out_dir = osp.basename(count[i]).replace('.', '_')
                out_dir = osp.join(osp.dirname(count[i]), out_dir)
                out_dir = osp.join(self.outputChange, out_dir)

                if not osp.exists(out_dir):
                    os.mkdir(out_dir)

                PIL.Image.fromarray(img).save(osp.join(out_dir, 'img.png'))

                utils.lblsave(osp.join(out_dir, 'label.png'), lbl)
                PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, 'label_viz.png'))

                with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
                    for lbl_name in label_names:
                        f.write(lbl_name + '\n')

                warnings.warn('info.yaml is being replaced by label_names.txt')
                info = dict(label_names=label_names)
                with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
                    yaml.safe_dump(info, f, default_flow_style=False)

                print('Saved to: %s' % out_dir)
        self.lineEdit_do_jsontodataset.setText('Json To Dataset Complete!')

    # <------------FUNC4：Get_JPG_PNG--------------->
    def select_Jsonjpg_2(self):
        dirname11 = QFileDialog.getExistingDirectory(self, "选择存放Json和Jpg文件的文件夹", '.')
        if dirname11:
            self.lineEdit_Jsonjpg_2.setText(dirname11)
            self.JsonjpgChange2 = dirname11 + '/'
            self.dirname111 = dirname11

    def select_classname(self):
        dirname12 = QFileDialog.getOpenFileName(self, '选择ClassName文件', './', "Txt Files (*.txt)")
        if dirname12:
            self.lineEdit_Jsonjpg_3.setText(dirname12[0])
            self.txt = dirname12[0]

    def select_jpg2(self):
        dirname13 = QFileDialog.getExistingDirectory(self, "选择存放Jpg图像的文件夹", '.')
        if dirname13:
            self.lineEdit_Jsonjpg_4.setText(dirname13)
            self.jpg2Change = dirname13

    def select_png2(self):
        dirname14 = QFileDialog.getExistingDirectory(self, "选择存放Png图像的文件夹", '.')
        if dirname14:
            self.lineEdit_Jsonjpg_5.setText(dirname14)
            self.pngChange = dirname14

    def select_out2(self):
        dirname15 = QFileDialog.getExistingDirectory(self, "选择JsonToDataset的结果文件夹", '.')
        if dirname15:
            self.lineEdit_Jsonjpg_7.setText(dirname15)
            self.out2Change = dirname15 + '/'

    def Get_jpg_png(self):
        # 读取原文件夹
        count = os.listdir(self.JsonjpgChange2)
        for i in range(0, len(count)):
            # 如果里的文件以jpg结尾
            # 则寻找它对应的png
            if count[i].endswith("jpg"):
                path = os.path.join(self.dirname111, count[i])
                img = Image.open(path)
                img.save(os.path.join(self.jpg2Change, count[i]))

                # 找到对应的png
                path = self.out2Change + count[i].split(".")[0] + "_json/label.png"
                img = Image.open(path)

                # 找到全局的类
                class_txt = open(self.txt, "r")
                class_name = class_txt.read().splitlines()
                # ["bk","cat","dog"]
                # 打开json文件里面存在的类，称其为局部类
                with open(self.out2Change + count[i].split(".")[0] + "_json/label_names.txt", "r") as f:
                    names = f.read().splitlines()
                    # ["bk","dog"]
                    new = Image.new("RGB", [np.shape(img)[1], np.shape(img)[0]])
                    for name in names:
                        # index_json是json文件里存在的类，局部类
                        index_json = names.index(name)
                        # index_all是全局的类
                        index_all = class_name.index(name)
                        # 将局部类转换成为全局类

                        new = new + np.expand_dims(index_all * (np.array(img) == index_json), -1)

                new = Image.fromarray(np.uint8(new))
                new.save(os.path.join(self.pngChange, count[i].replace("jpg", "png")))
                print(np.max(new), np.min(new))
        self.lineEdit_Jsonjpg_6.setText('Get JPG and PNG Complete!!!')

    def exitApp(self):
        # self.camera.release()
        QCoreApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Seg_Tool()
    ui.show()
    sys.exit(app.exec_())
