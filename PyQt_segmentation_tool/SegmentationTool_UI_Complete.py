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

# from SegmentationTool import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1304, 963)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(898, 840, 101, 61))
        self.exit_button.setObjectName("exit_button")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 0, 231, 61))
        self.label_2.setStyleSheet("font: 18pt \"AcadEref\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 210, 261, 61))
        self.label_3.setStyleSheet("font: 18pt \"Times New Roman\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(738, 240, 391, 61))
        self.label_4.setStyleSheet("font: 18pt \"AcadEref\";")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(850, 530, 221, 61))
        self.label_5.setStyleSheet("font: 18pt \"Times New Roman\";")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 430, 261, 61))
        self.label_6.setStyleSheet("font: 18pt \"Times New Roman\";")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(40, 610, 601, 61))
        self.label_7.setStyleSheet("font: 18pt \"Times New Roman\";")
        self.label_7.setObjectName("label_7")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(688, 590, 511, 241))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.sel_model_label = QtWidgets.QPushButton(self.layoutWidget)
        self.sel_model_label.setObjectName("sel_model_label")
        self.gridLayout_4.addWidget(self.sel_model_label, 0, 0, 1, 1)
        self.lineEdit_modellabel = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_modellabel.setText("")
        self.lineEdit_modellabel.setObjectName("lineEdit_modellabel")
        self.gridLayout_4.addWidget(self.lineEdit_modellabel, 0, 1, 1, 1)
        self.sel_handle_label = QtWidgets.QPushButton(self.layoutWidget)
        self.sel_handle_label.setObjectName("sel_handle_label")
        self.gridLayout_4.addWidget(self.sel_handle_label, 1, 0, 1, 1)
        self.lineEdit_handlelabel = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_handlelabel.setText("")
        self.lineEdit_handlelabel.setObjectName("lineEdit_handlelabel")
        self.gridLayout_4.addWidget(self.lineEdit_handlelabel, 1, 1, 1, 1)
        self.compute_iou = QtWidgets.QPushButton(self.layoutWidget)
        self.compute_iou.setObjectName("compute_iou")
        self.gridLayout_4.addWidget(self.compute_iou, 2, 0, 1, 1)
        self.textEdit_iou = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit_iou.setObjectName("textEdit_iou")
        self.gridLayout_4.addWidget(self.textEdit_iou, 2, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(70, 280, 511, 141))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sel_jsonjpg_file = QtWidgets.QPushButton(self.layoutWidget1)
        self.sel_jsonjpg_file.setObjectName("sel_jsonjpg_file")
        self.gridLayout_2.addWidget(self.sel_jsonjpg_file, 0, 0, 1, 1)
        self.lineEdit_jsonjpg = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_jsonjpg.setObjectName("lineEdit_jsonjpg")
        self.gridLayout_2.addWidget(self.lineEdit_jsonjpg, 0, 1, 1, 1)
        self.sel_jsonsave_file = QtWidgets.QPushButton(self.layoutWidget1)
        self.sel_jsonsave_file.setObjectName("sel_jsonsave_file")
        self.gridLayout_2.addWidget(self.sel_jsonsave_file, 1, 0, 1, 1)
        self.lineEdit_json = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_json.setObjectName("lineEdit_json")
        self.gridLayout_2.addWidget(self.lineEdit_json, 1, 1, 1, 1)
        self.sel_jpgsave_file = QtWidgets.QPushButton(self.layoutWidget1)
        self.sel_jpgsave_file.setObjectName("sel_jpgsave_file")
        self.gridLayout_2.addWidget(self.sel_jpgsave_file, 2, 0, 1, 1)
        self.lineEdit_jpg = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_jpg.setObjectName("lineEdit_jpg")
        self.gridLayout_2.addWidget(self.lineEdit_jpg, 2, 1, 1, 1)
        self.json_jpg_change = QtWidgets.QPushButton(self.layoutWidget1)
        self.json_jpg_change.setObjectName("json_jpg_change")
        self.gridLayout_2.addWidget(self.json_jpg_change, 3, 0, 1, 1)
        self.lineEdit_jsonjpg_change = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_jsonjpg_change.setObjectName("lineEdit_jsonjpg_change")
        self.gridLayout_2.addWidget(self.lineEdit_jsonjpg_change, 3, 1, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(70, 60, 511, 151))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.sel_video_file = QtWidgets.QPushButton(self.layoutWidget2)
        self.sel_video_file.setObjectName("sel_video_file")
        self.gridLayout.addWidget(self.sel_video_file, 0, 0, 1, 1)
        self.lineEdit_video = QtWidgets.QLineEdit(self.layoutWidget2)
        self.lineEdit_video.setObjectName("lineEdit_video")
        self.gridLayout.addWidget(self.lineEdit_video, 0, 1, 1, 1)
        self.sel_savepic_file = QtWidgets.QPushButton(self.layoutWidget2)
        self.sel_savepic_file.setObjectName("sel_savepic_file")
        self.gridLayout.addWidget(self.sel_savepic_file, 1, 0, 1, 1)
        self.lineEdit_image = QtWidgets.QLineEdit(self.layoutWidget2)
        self.lineEdit_image.setObjectName("lineEdit_image")
        self.gridLayout.addWidget(self.lineEdit_image, 1, 1, 1, 1)
        self.video_pic_change = QtWidgets.QPushButton(self.layoutWidget2)
        self.video_pic_change.setObjectName("video_pic_change")
        self.gridLayout.addWidget(self.video_pic_change, 2, 0, 1, 1)
        self.lineEdit_videopic_change = QtWidgets.QLineEdit(self.layoutWidget2)
        self.lineEdit_videopic_change.setObjectName("lineEdit_videopic_change")
        self.gridLayout.addWidget(self.lineEdit_videopic_change, 2, 1, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(688, 300, 511, 232))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_valtrain = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_valtrain.setText("")
        self.lineEdit_valtrain.setObjectName("lineEdit_valtrain")
        self.gridLayout_3.addWidget(self.lineEdit_valtrain, 4, 2, 1, 1)
        self.train_val_change = QtWidgets.QPushButton(self.layoutWidget3)
        self.train_val_change.setObjectName("train_val_change")
        self.gridLayout_3.addWidget(self.train_val_change, 5, 0, 1, 1)
        self.lineEdit_trainimage = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_trainimage.setObjectName("lineEdit_trainimage")
        self.gridLayout_3.addWidget(self.lineEdit_trainimage, 0, 2, 1, 1)
        self.sel_vallabel_file = QtWidgets.QPushButton(self.layoutWidget3)
        self.sel_vallabel_file.setObjectName("sel_vallabel_file")
        self.gridLayout_3.addWidget(self.sel_vallabel_file, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.layoutWidget3)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 4, 0, 1, 2)
        self.lineEdit_valimage = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_valimage.setObjectName("lineEdit_valimage")
        self.gridLayout_3.addWidget(self.lineEdit_valimage, 2, 2, 1, 1)
        self.sel_trainlabel_file = QtWidgets.QPushButton(self.layoutWidget3)
        self.sel_trainlabel_file.setObjectName("sel_trainlabel_file")
        self.gridLayout_3.addWidget(self.sel_trainlabel_file, 1, 0, 1, 2)
        self.sel_trainimage_file = QtWidgets.QPushButton(self.layoutWidget3)
        self.sel_trainimage_file.setObjectName("sel_trainimage_file")
        self.gridLayout_3.addWidget(self.sel_trainimage_file, 0, 0, 1, 2)
        self.sel_valimage_file = QtWidgets.QPushButton(self.layoutWidget3)
        self.sel_valimage_file.setObjectName("sel_valimage_file")
        self.gridLayout_3.addWidget(self.sel_valimage_file, 2, 0, 1, 2)
        self.lineEdit_trainval_change = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_trainval_change.setObjectName("lineEdit_trainval_change")
        self.gridLayout_3.addWidget(self.lineEdit_trainval_change, 5, 1, 1, 2)
        self.lineEdit_trainlabel = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_trainlabel.setObjectName("lineEdit_trainlabel")
        self.gridLayout_3.addWidget(self.lineEdit_trainlabel, 1, 2, 1, 1)
        self.lineEdit_vallabel = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEdit_vallabel.setObjectName("lineEdit_vallabel")
        self.gridLayout_3.addWidget(self.lineEdit_vallabel, 3, 2, 1, 1)
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(70, 500, 511, 101))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.sel_Jsonjpg = QtWidgets.QPushButton(self.layoutWidget4)
        self.sel_Jsonjpg.setObjectName("sel_Jsonjpg")
        self.gridLayout_5.addWidget(self.sel_Jsonjpg, 0, 0, 1, 1)
        self.lineEdit_Jsonjpg = QtWidgets.QLineEdit(self.layoutWidget4)
        self.lineEdit_Jsonjpg.setObjectName("lineEdit_Jsonjpg")
        self.gridLayout_5.addWidget(self.lineEdit_Jsonjpg, 0, 1, 1, 1)
        self.sel_output = QtWidgets.QPushButton(self.layoutWidget4)
        self.sel_output.setObjectName("sel_output")
        self.gridLayout_5.addWidget(self.sel_output, 1, 0, 1, 1)
        self.lineEdit_output = QtWidgets.QLineEdit(self.layoutWidget4)
        self.lineEdit_output.setText("")
        self.lineEdit_output.setObjectName("lineEdit_output")
        self.gridLayout_5.addWidget(self.lineEdit_output, 1, 1, 1, 1)
        self.Do_jsontodataset = QtWidgets.QPushButton(self.layoutWidget4)
        self.Do_jsontodataset.setObjectName("Do_jsontodataset")
        self.gridLayout_5.addWidget(self.Do_jsontodataset, 2, 0, 1, 1)
        self.lineEdit_do_jsontodataset = QtWidgets.QLineEdit(self.layoutWidget4)
        self.lineEdit_do_jsontodataset.setObjectName("lineEdit_do_jsontodataset")
        self.gridLayout_5.addWidget(self.lineEdit_do_jsontodataset, 2, 1, 1, 1)
        self.layoutWidget5 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget5.setGeometry(QtCore.QRect(70, 670, 521, 205))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.layoutWidget5)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.sel_Jsonjpg_2 = QtWidgets.QPushButton(self.layoutWidget5)
        self.sel_Jsonjpg_2.setObjectName("sel_Jsonjpg_2")
        self.gridLayout_6.addWidget(self.sel_Jsonjpg_2, 0, 0, 1, 2)
        self.lineEdit_Jsonjpg_2 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.lineEdit_Jsonjpg_2.setObjectName("lineEdit_Jsonjpg_2")
        self.gridLayout_6.addWidget(self.lineEdit_Jsonjpg_2, 0, 2, 1, 1)
        self.sel_Output_file = QtWidgets.QPushButton(self.layoutWidget5)
        self.sel_Output_file.setObjectName("sel_Output_file")
        self.gridLayout_6.addWidget(self.sel_Output_file, 1, 0, 1, 1)
        self.lineEdit_Jsonjpg_7 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.lineEdit_Jsonjpg_7.setText("")
        self.lineEdit_Jsonjpg_7.setObjectName("lineEdit_Jsonjpg_7")
        self.gridLayout_6.addWidget(self.lineEdit_Jsonjpg_7, 1, 1, 1, 2)
        self.sel_Classname_file = QtWidgets.QPushButton(self.layoutWidget5)
        self.sel_Classname_file.setObjectName("sel_Classname_file")
        self.gridLayout_6.addWidget(self.sel_Classname_file, 2, 0, 1, 1)
        self.lineEdit_Jsonjpg_3 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.lineEdit_Jsonjpg_3.setObjectName("lineEdit_Jsonjpg_3")
        self.gridLayout_6.addWidget(self.lineEdit_Jsonjpg_3, 2, 2, 1, 1)
        self.sel_JPG_file = QtWidgets.QPushButton(self.layoutWidget5)
        self.sel_JPG_file.setObjectName("sel_JPG_file")
        self.gridLayout_6.addWidget(self.sel_JPG_file, 3, 0, 1, 1)
        self.lineEdit_Jsonjpg_4 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.lineEdit_Jsonjpg_4.setObjectName("lineEdit_Jsonjpg_4")
        self.gridLayout_6.addWidget(self.lineEdit_Jsonjpg_4, 3, 2, 1, 1)
        self.sel_PNG_file = QtWidgets.QPushButton(self.layoutWidget5)
        self.sel_PNG_file.setObjectName("sel_PNG_file")
        self.gridLayout_6.addWidget(self.sel_PNG_file, 4, 0, 1, 1)
        self.lineEdit_Jsonjpg_5 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.lineEdit_Jsonjpg_5.setObjectName("lineEdit_Jsonjpg_5")
        self.gridLayout_6.addWidget(self.lineEdit_Jsonjpg_5, 4, 2, 1, 1)
        self.do_get_jpgpng = QtWidgets.QPushButton(self.layoutWidget5)
        self.do_get_jpgpng.setObjectName("do_get_jpgpng")
        self.gridLayout_6.addWidget(self.do_get_jpgpng, 5, 0, 1, 1)
        self.lineEdit_Jsonjpg_6 = QtWidgets.QLineEdit(self.layoutWidget5)
        self.lineEdit_Jsonjpg_6.setObjectName("lineEdit_Jsonjpg_6")
        self.gridLayout_6.addWidget(self.lineEdit_Jsonjpg_6, 5, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(820, 0, 231, 61))
        self.label_8.setStyleSheet("font: 18pt \"AcadEref\";")
        self.label_8.setObjectName("label_8")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(688, 60, 511, 170))
        self.widget.setObjectName("widget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_7.addWidget(self.pushButton, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_7.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_7.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_7.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_7.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_7.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_7.addWidget(self.pushButton_4, 3, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_7.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_7.addWidget(self.pushButton_5, 4, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_7.addWidget(self.lineEdit_5, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1304, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.exit_button.setText(_translate("MainWindow", "退出"))
        self.label_2.setText(_translate("MainWindow", "视频转图像功能"))
        self.label_3.setText(_translate("MainWindow", "JSON/JPG文件分离"))
        self.label_4.setText(_translate("MainWindow", "从训练集随机选择比例测试集"))
        self.label_5.setText(_translate("MainWindow", "MIOU/MPA计算"))
        self.label_6.setText(_translate("MainWindow", "JSON_TO_Dataset"))
        self.label_7.setText(_translate("MainWindow", "Get_JPG_PNG(从Dtaset提取训练图像和标签)"))
        self.sel_model_label.setText(_translate("MainWindow", "点击选择模型输出标签图像文件夹"))
        self.sel_handle_label.setText(_translate("MainWindow", "点击选择人工标签图像文件夹"))
        self.compute_iou.setText(_translate("MainWindow", "点击选择IOU等参数"))
        self.sel_jsonjpg_file.setText(_translate("MainWindow", "选择JSON-JPG素材文件夹"))
        self.sel_jsonsave_file.setText(_translate("MainWindow", "点击选择JSON存储文件夹"))
        self.sel_jpgsave_file.setText(_translate("MainWindow", "点击选择JPG存储文件夹"))
        self.json_jpg_change.setText(_translate("MainWindow", "开始转移"))
        self.sel_video_file.setText(_translate("MainWindow", "点击选择视频文件"))
        self.sel_savepic_file.setText(_translate("MainWindow", "点击选择存储图像文件夹"))
        self.video_pic_change.setText(_translate("MainWindow", "开始转换"))
        self.train_val_change.setText(_translate("MainWindow", "开始随机转移"))
        self.sel_vallabel_file.setText(_translate("MainWindow", "点击选择测试集标签文件夹"))
        self.label.setText(_translate("MainWindow", "输入验证集/训练集的比例："))
        self.sel_trainlabel_file.setText(_translate("MainWindow", "点击选择训练集标签文件夹"))
        self.sel_trainimage_file.setText(_translate("MainWindow", "点击选择训练集图像文件夹"))
        self.sel_valimage_file.setText(_translate("MainWindow", "点击选择测试集图像文件夹"))
        self.sel_Jsonjpg.setText(_translate("MainWindow", "点击选择JSON&JPG文件夹"))
        self.sel_output.setText(_translate("MainWindow", "点击选择OUTPUT文件夹"))
        self.Do_jsontodataset.setText(_translate("MainWindow", "执行JsonToDataset"))
        self.sel_Jsonjpg_2.setText(_translate("MainWindow", "点击选择JSON&JPG文件夹"))
        self.sel_Output_file.setText(_translate("MainWindow", "点击选择OUTPUT文件夹"))
        self.sel_Classname_file.setText(_translate("MainWindow", "点击选择ClassName文件"))
        self.sel_JPG_file.setText(_translate("MainWindow", "点击选择输出JPG文件夹"))
        self.sel_PNG_file.setText(_translate("MainWindow", "点击选择输出PNG文件夹"))
        self.do_get_jpgpng.setText(_translate("MainWindow", "执行Get_JPG_PNG"))
        self.label_8.setText(_translate("MainWindow", "数据扩增(亮度)"))
        self.pushButton.setText(_translate("MainWindow", "点击选择训练图像文件夹"))
        self.pushButton_2.setText(_translate("MainWindow", "点击选择训练标签文件夹"))
        self.pushButton_3.setText(_translate("MainWindow", "点击选择扩增图像文件夹"))
        self.pushButton_4.setText(_translate("MainWindow", "点击选择扩增标签文件夹"))
        self.pushButton_5.setText(_translate("MainWindow", "点击选择扩增标签文件夹"))








import sys
import threading
import time, logging
import numpy as np
import os, random, shutil

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import cv2
from PyQt5.QtCore import QTimer, QCoreApplication
from PIL import Image, ImageEnhance, ImageOps, ImageFile
import argparse
import json
import os.path as osp
import warnings
import PIL.Image
import yaml
from labelme import utils
# import draw
import base64
import io
import PIL.ImageDraw





__all__ = ['SegmentationMetric']
logger = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True
opsList = {"randomColor", "randomGaussian"}  # "randomRotation",


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
        self.pushButton.clicked.connect(self.select_trainimage)
        self.pushButton_2.clicked.connect(self.select_trainlabel)
        self.pushButton_3.clicked.connect(self.select_newimage)
        self.pushButton_4.clicked.connect(self.select_newlabel)
        self.pushButton_5.clicked.connect(self.DataAug)
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
                frame = cv2.resize(frame, (640, 320))
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
        file_list = []  # 读取文件，并将地址、图片名和标签写到txt文件中
        write_file = open(write_file_name, "w")  # 打开write_file_name文件
        for file in os.listdir(Image_dir):
            if file.endswith(".json"):
                name = file.split('.')[0]  # JSON名称和后缀名
                write_name = name
                file_list.append(write_name)
        sorted(file_list)  # 将列表中所有元素随机排列
        number_of_lines = len(file_list)
        for current_line in range(number_of_lines):
            write_file.write(file_list[current_line] + '\n')
        write_file.close()

    def moveJPG(self, fileLabelDir, write_file_name):
        pathDir = os.listdir(fileLabelDir)
        f = open(write_file_name, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')  # 去除文本的换行符，否则报错
            shutil.move(fileLabelDir + str(line) + '.jpg', self.SaveJpgChange + str(line) + '.jpg')

    def moveJSON(self, fileLabelDir, write_file_name):
        pathDir = os.listdir(fileLabelDir)
        f = open(write_file_name, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')  # 去除文本的换行符，否则报错
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
        write_file = open(write_file_name, "w")  # 打开write_file_name文件
        for file in os.listdir(Image_dir):
            if file.endswith(".jpg"):
                name = file.split('.')[0]  # 分割图像名称和后缀名
                write_name = name
                file_list.append(write_name)
        sorted(file_list)  # 将列表中所有元素随机排列
        number_of_lines = len(file_list)
        for current_line in range(number_of_lines):
            write_file.write(file_list[current_line] + '\n')
        write_file.close()

    def moveLabel(self, fileLabelDir, write_file_name):
        pathDir = os.listdir(fileLabelDir)
        f = open(write_file_name, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')  # 去除文本的换行符，否则报错
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
        return classAcc  # 返回的是一个列表值，如：[0.90, 0.80, 0.96]，表示类别1 2 3各类别的预测准确率

    def meanPixelAccuracy(self):
        classAcc = self.classPixelAccuracy()
        meanAcc = np.nanmean(classAcc)  # np.nanmean 求平均值，nan表示遇到Nan类型，其值取为0
        return meanAcc  # 返回单个值，如：np.nanmean([0.90, 0.80, 0.96, nan, nan]) = (0.90 + 0.80 + 0.96） / 3 =  0.89

    def meanIntersectionOverUnion(self):
        # Intersection = TP Union = TP + FP + FN
        # IoU = TP / (TP + FP + FN)
        intersection = np.diag(self.confusionMatrix)  # 取对角元素的值，返回列表
        union = np.sum(self.confusionMatrix, axis=1) + np.sum(self.confusionMatrix, axis=0) - np.diag(
                self.confusionMatrix)  # axis = 1表示混淆矩阵行的值，返回列表； axis = 0表示取混淆矩阵列的值，返回列表
        IoU = intersection / union  # 返回列表，其值为各个类别的IoU
        mIoU = np.nanmean(IoU)  # 求各类别IoU的平均
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
                name = file.split('.')[0]  # 分割图像名称和后缀名
                write_name = name
                file_list.append(write_name)
        sorted(file_list)  # 将列表中所有元素随机排列
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
                lbl_viz = self.draw_label(lbl, img, captions)
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

    def label_colormap(self,N=256):

        def bitget(byteval, idx):
            return ((byteval & (1 << idx)) != 0)

        cmap = np.zeros((N, 3))
        for i in range(0, N):
            id = i
            r, g, b = 0, 0, 0
            for j in range(0, 8):
                r = np.bitwise_or(r, (bitget(id, 0) << 7 - j))
                g = np.bitwise_or(g, (bitget(id, 1) << 7 - j))
                b = np.bitwise_or(b, (bitget(id, 2) << 7 - j))
                id = (id >> 3)
            cmap[i, 0] = r
            cmap[i, 1] = g
            cmap[i, 2] = b
        cmap = cmap.astype(np.float32) / 255
        return cmap


    # similar function as skimage.color.label2rgb
    def label2rgb(self,lbl, img=None, n_labels=None, alpha=0.5, thresh_suppress=0):
        if n_labels is None:
            n_labels = len(np.unique(lbl))

        cmap = self.label_colormap(n_labels)
        cmap = (cmap * 255).astype(np.uint8)

        lbl_viz = cmap[lbl]
        lbl_viz[lbl == -1] = (0, 0, 0)  # unlabeled

        if img is not None:
            img_gray = PIL.Image.fromarray(img).convert('LA')
            img_gray = np.asarray(img_gray.convert('RGB'))
            # img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            # img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
            lbl_viz = alpha * lbl_viz + (1 - alpha) * img_gray
            lbl_viz = lbl_viz.astype(np.uint8)

        return lbl_viz


    def draw_label(self,label, img=None, label_names=None, colormap=None):
        import matplotlib.pyplot as plt
        backend_org = plt.rcParams['backend']
        plt.switch_backend('agg')

        plt.subplots_adjust(left=0, right=1, top=1, bottom=0,
                            wspace=0, hspace=0)
        plt.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

        if label_names is None:
            label_names = [str(l) for l in range(label.max() + 1)]

        if colormap is None:
            colormap = self.label_colormap(len(label_names))

        label_viz = self.label2rgb(label, img, n_labels=len(label_names))
        plt.imshow(label_viz)
        plt.axis('off')

        plt_handlers = []
        plt_titles = []
        for label_value, label_name in enumerate(label_names):
            if label_value not in label:
                continue
            if label_name.startswith('_'):
                continue
            fc = colormap[label_value]
            p = plt.Rectangle((0, 0), 1, 1, fc=fc)
            plt_handlers.append(p)
            plt_titles.append('{value}: {name}'
                              .format(value=label_value, name=label_name))
        plt.legend(plt_handlers, plt_titles, loc='lower right', framealpha=.5)

        f = io.BytesIO()
        plt.savefig(f, bbox_inches='tight', pad_inches=0)
        plt.cla()
        plt.close()

        plt.switch_backend(backend_org)

        out_size = (label_viz.shape[1], label_viz.shape[0])
        out = PIL.Image.open(f).resize(out_size, PIL.Image.BILINEAR).convert('RGB')
        out = np.asarray(out)
        return out


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
    ######################################
    def openImage(self, image):
        return Image.open(image, mode="r")

    def randomColor(self, image, label):
        """
        对图像进行颜色抖动
        :param image: PIL的图像image
        :return: 有颜色色差的图像image
        """
        # random_factor = np.random.randint(0, 31) / 10.  # 随机因子
        # color_image = ImageEnhance.Color(image).enhance(random_factor)  # 调整图像的饱和度
        random_factor = np.random.randint(10, 12) / 10.  # 随机因子
        return ImageEnhance.Brightness(image).enhance(random_factor) ,label  # 调整图像的亮度


    def randomGaussian(self, image, label, mean=0.2, sigma=0.3):
        """
         对图像进行高斯噪声处理
        :param image:
        :return:
        """

        def gaussianNoisy(im, mean=0.2, sigma=0.3):
            """
            对图像做高斯噪音处理
            :param im: 单通道图像
            :param mean: 偏移量
            :param sigma: 标准差
            :return:
            """
            for _i in range(len(im)):
                im[_i] += random.gauss(mean, sigma)
            return im

        # 将图像转化成数组
        img = np.asarray(image)
        img.flags.writeable = True  # 将数组改为读写模式
        width, height = img.shape[:2]
        img_r = gaussianNoisy(img[:, :, 0].flatten(), mean, sigma)
        img_g = gaussianNoisy(img[:, :, 1].flatten(), mean, sigma)
        img_b = gaussianNoisy(img[:, :, 2].flatten(), mean, sigma)
        img[:, :, 0] = img_r.reshape([width, height])
        img[:, :, 1] = img_g.reshape([width, height])
        img[:, :, 2] = img_b.reshape([width, height])
        return Image.fromarray(np.uint8(img)), label


    def saveImage(self, image, path):
        image.save(path)

    def imageOps(self, func_name, image, label, img_des_path, label_des_path , img_file_name, label_file_name, times=5):
        funcMap = {
                   "randomColor": self.randomColor,
                   "randomGaussian": self.randomGaussian
                   }
        if funcMap.get(func_name) is None:
            logger.error("%s is not exist", func_name)
            return -1

        for _i in range(0, times, 1):
            new_image , new_label = funcMap[func_name](image,label)
            self.saveImage(new_image, os.path.join(img_des_path, func_name + str(_i) + img_file_name))
            self.saveImage(new_label, os.path.join(label_des_path, func_name + str(_i) + label_file_name))


    def threadOPS(self,img_path, new_img_path, label_path, new_label_path):
        """
        多线程处理事务
        :param src_path: 资源文件
        :param des_path: 目的地文件
        :return:
        """
        #img path
        if os.path.isdir(img_path):
            img_names = os.listdir(img_path)
        else:
            img_names = [img_path]

        #label path
        if os.path.isdir(label_path):
            label_names = os.listdir(label_path)
        else:
            label_names = [label_path]

        img_num = 0
        label_num = 0

        #img num
        for img_name in img_names:
            tmp_img_name = os.path.join(img_path, img_name)
            if os.path.isdir(tmp_img_name):
                print('contain file folder')
                exit()
            else:
                img_num = img_num + 1;
        #label num
        for label_name in label_names:
            tmp_label_name = os.path.join(label_path, label_name)
            if os.path.isdir(tmp_label_name):
                print('contain file folder')
                exit()
            else:
                label_num = label_num + 1

        if img_num != label_num:
            print('the num of img and label is not equl')
            exit()
        else:
            num = img_num


        for i in range(num):
            img_name = img_names[i]
            print(img_name)
            label_name = label_names[i]
            print (label_name)

            tmp_img_name = os.path.join(img_path, img_name)
            tmp_label_name = os.path.join(label_path, label_name)

            # 读取文件并进行操作
            image = self.openImage(tmp_img_name)
            label = self.openImage(tmp_label_name)

            threadImage = [0] * 5
            _index = 0
            for ops_name in opsList:
                threadImage[_index] = threading.Thread(target=self.imageOps,
                                                        args=(ops_name, image, label, new_img_path, new_label_path, img_name, label_name))
                threadImage[_index].start()
                _index += 1
                time.sleep(0.2)

    def select_trainimage(self):
        dirname21 = QFileDialog.getExistingDirectory(self, "选择训练图像文件夹", '.')
        if dirname21:
            self.lineEdit.setText(dirname21)
            self.outputtrainimage = dirname21

    def select_newimage(self):
        dirname22 = QFileDialog.getExistingDirectory(self, "选择训练标签文件夹", '.')
        if dirname22:
            self.lineEdit_3.setText(dirname22)
            self.outputnewimage = dirname22

    def select_trainlabel(self):
        dirname23 = QFileDialog.getExistingDirectory(self, "选择扩增图像文件夹", '.')
        if dirname23:
            self.lineEdit_2.setText(dirname23)
            self.outputtrainlabel = dirname23

    def select_newlabel(self):
        dirname24 = QFileDialog.getExistingDirectory(self, "选择扩增标签文件夹", '.')
        if dirname24:
            self.lineEdit_4.setText(dirname24)
            self.outputnewlabel = dirname24


    def DataAug(self):
        self.threadOPS(self.outputtrainimage,
              self.outputnewimage,
              self.outputtrainlabel,
              self.outputnewlabel)
        self.lineEdit_5.setText('Data Augment Finish！！！')

    def exitApp(self):
        # self.camera.release()
        QCoreApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Seg_Tool()
    ui.show()
    sys.exit(app.exec_())
