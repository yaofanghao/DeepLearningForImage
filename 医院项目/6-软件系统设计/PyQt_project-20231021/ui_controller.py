"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/10/24 11:34
    @Filename: ui_controller.py
    @Software: PyCharm

    合并并重构后的 UI 控制模块：
      - InitUi       — 初始界面
      - InfoUi       — 诊断报告填写界面（Bug 修复）
      - BasePredictUi — 预测模块基类（抽取公共逻辑）
      - ChanghuaUi   — 肠化亚型辅助诊断模块（继承 BasePredictUi）
      - OLGIMUi      — OLGIM 综合评估模块（继承 BasePredictUi）
"""
import os
import time
import logging

import numpy as np
from PIL import Image
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QProgressDialog
from PyQt5.QtGui import QPixmap

from config import (
    OUTPUT_DIR_CHANGHUA, OUTPUT_DIR_OLGIM, OUTPUT_DIR_INFO_REPORT, FONT_PATH
)
from model_loader import ModelManager

# UI 界面文件
from widgets.InitWidget import Ui_widget as init_Ui
from widgets.InfoWidget import Ui_Form as info_Ui
from widgets.ChanghuaWidget import Ui_Form as ChanghuaUiForm
from widgets.OLGIMWidget import Ui_Form as OlgimUiForm

logger = logging.getLogger(__name__)


# ===================== 初始界面 InitWidget =====================
class InitUi(QtWidgets.QMainWindow, init_Ui):
    switch_changhua = QtCore.pyqtSignal()
    switch_olgim = QtCore.pyqtSignal()

    def __init__(self):
        super(InitUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.go_changhua)
        self.pushButton2.clicked.connect(self.go_olgim)
        self.pushButton3.clicked.connect(self.close_dialog)

    def go_changhua(self):
        self.switch_changhua.emit()

    def go_olgim(self):
        self.switch_olgim.emit()

    def close_dialog(self):
        reply = QMessageBox.warning(
            self, "提示", "是否确定退出",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.close()


# ===================== 诊断报告填写 InfoWidget =====================
class InfoUi(QtWidgets.QMainWindow, info_Ui):
    def __init__(self):
        super(InfoUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.save_info)
        self.pushButton2.clicked.connect(self.gen_report)
        self.pushButton3.clicked.connect(self.close_dialog)

        self.output_pdf_dir = OUTPUT_DIR_INFO_REPORT
        if not os.path.exists(self.output_pdf_dir):
            os.makedirs(self.output_pdf_dir)
        self.now = QtCore.QDate.currentDate()
        self.lineEdit12.setText(self.now.toString('yyyy-MM-dd'))

    def close_dialog(self):
        reply = QMessageBox.warning(
            self, "提示", "是否确定退出",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.close()

    def save_info(self):
        print(self.textEdit.toPlainText())
        QMessageBox.about(self, "提示", self.tr("信息保存成功！"))

    def gen_report(self):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen import canvas

        pdfmetrics.registerFont(TTFont('font1', FONT_PATH))

        filename, _ = QFileDialog.getSaveFileName(
            self, 'save file', self.output_pdf_dir, "ALL (*.pdf)"
        )
        dst = os.path.join(self.output_pdf_dir, filename.replace(".jpg", ".pdf"))

        pdf_file = canvas.Canvas(dst, pagesize=A4)
        pdf_file.setFont("font1", 10)
        pdf_file.setFillColorRGB(0, 0, 0, 1)
        w, h = A4

        menzhenhao = self.lineEdit1.text()
        zhuyuanhao = self.lineEdit2.text()
        binglihao = self.lineEdit3.text()
        jianchahao = self.lineEdit4.text()
        name = self.lineEdit5.text()
        sex = self.lineEdit6.text()
        age = self.lineEdit7.text()
        ke = self.lineEdit8.text()
        chuang = self.lineEdit9.text()
        origin = self.lineEdit10.text()
        baogaoyishi = self.lineEdit11.text()
        chubuzhenduan = self.textEdit.toPlainText()
        date = self.lineEdit12.text()

        pdf_file.drawString(
            50, h - 50,
            "门诊号：" + str(menzhenhao) +
            "    " + "住院号：" + str(zhuyuanhao) +
            "    " + "病历号：" + str(binglihao) +
            "    " + "检查号：" + str(jianchahao),
        )
        pdf_file.drawString(
            50, h - 100,
            "-----------------------------------------------------")
        pdf_file.drawString(
            50, h - 150,
            "姓名：" + str(name) +
            "    " + "性别：" + str(sex) +
            "    " + "年龄：" + str(age),
        )
        pdf_file.drawString(
            50, h - 200,
            "科别：" + str(ke) +
            "    " + "床号：" + str(chuang) +
            "    " + "来源：" + str(origin),
        )
        pdf_file.drawString(
            50, h - 250,
            "-----------------------------------------------------")
        pdf_file.drawString(
            50, h - 300,
            "初步诊断所见：" + str(chubuzhenduan))
        pdf_file.drawString(
            50, h - 500,
            "-----------------------------------------------------")
        pdf_file.drawString(
            50, h - 550,
            "报告医师：" + str(baogaoyishi))
        pdf_file.drawString(50, h - 600, "日期：" + str(date))

        pdf_file.save()
        QMessageBox.about(self, "提示", self.tr("报告保存成功！"))


# ===================== 预测模块基类 =====================
class BasePredictUi:
    """
    预测界面公共逻辑基类（Mixin）。
    子类需保证创建了以下属性 / UI 控件:
      - self.file_paths, self.file_index, self.scores, self.output_dir
      - self.label5, self.label6, self.lineEdit2, self.lineEdit3, self.lineEdit5
      - self.pushButton1 ~ pushButton8 (对应按钮)
      - self.switch_init, self.switch_info (信号)
    """

    def __init__(self):
        self.pbar = None
        self.file_paths = []
        self.file_index = 0
        self.scores = []

    # ----- 页面跳转 -----
    def go_init(self):
        self.switch_init.emit()

    def write_report(self):
        self.switch_info.emit()

    # ----- 退出对话框 -----
    def close_dialog(self):
        reply = QMessageBox.warning(
            self, "提示", "是否确定退出",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.close()

    # ----- 导入文件夹 -----
    def import_folder(self):
        cur_dir = QtCore.QDir.currentPath()
        dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹', cur_dir)
        if not dir_path:
            return
        self.file_paths.clear()
        for root, _dirs, files in os.walk(dir_path, topdown=False):
            for f in files:
                self.file_paths.append(os.path.join(root, f))
        if not self.file_paths:
            return
        self.file_index = 0
        self._show_current_image()

    # ----- 图片切换（上 / 下一张） -----
    def folder_next(self):
        self.file_index += 1
        if self.file_index >= len(self.file_paths):
            QMessageBox.warning(self, "提示", self.tr("已经是最后一个！"))
            self.file_index = len(self.file_paths) - 1
        if not self.file_paths or self.file_index >= len(self.file_paths):
            return
        self._show_current_image()

    def folder_previous(self):
        self.file_index -= 1
        if self.file_index < 0:
            QMessageBox.warning(self, "提示", self.tr("已经是第一个！"))
            self.file_index = 0
        if not self.file_paths or self.file_index >= len(self.file_paths):
            return
        self._show_current_image()

    def _show_current_image(self):
        """显示当前索引的图片及对应的预测结果"""
        cur_path = self.file_paths[self.file_index]
        _filepath, filename = os.path.split(cur_path)
        # 显示原图
        img = QPixmap(cur_path).scaled(
            self.label5.width(), self.label5.height())
        self.label5.setPixmap(img)
        self.lineEdit5.setText(filename)
        # 显示置信度（避免索引越界）
        if self.file_index < len(self.scores):
            self.lineEdit3.setText(str(self.scores[self.file_index]))
        # 显示预测结果图（若已存在）
        predict_path = os.path.join(
            self.output_dir, filename.replace(".jpg", ".png"))
        if os.path.exists(predict_path):
            img_out = QPixmap(predict_path).scaled(
                self.label6.width(), self.label6.height())
            self.label6.setPixmap(img_out)

    # ----- 保存并显示预测结果 -----
    def save_jpg(self):
        if not self.file_paths:
            return
        cur_path = self.file_paths[self.file_index]
        _filepath, filename = os.path.split(cur_path)
        predict_path = os.path.join(
            self.output_dir, filename.replace(".jpg", ".png"))
        if os.path.exists(predict_path):
            img_out = QPixmap(predict_path).scaled(
                self.label6.width(), self.label6.height())
            self.label6.setPixmap(img_out)
        if self.file_index < len(self.scores):
            self.lineEdit3.setText(str(self.scores[self.file_index]))
        QMessageBox.about(self, "提示", self.tr("图片已保存，分类至指定文件夹！"))

    # ----- 批量预测（由子类实现） -----
    def predict_jpg(self):
        raise NotImplementedError


# ===================== 肠化亚型辅助诊断模块 =====================
class ChanghuaUi(QtWidgets.QMainWindow, ChanghuaUiForm, BasePredictUi):
    switch_init = QtCore.pyqtSignal()
    switch_info = QtCore.pyqtSignal()

    def __init__(self):
        super(ChanghuaUi, self).__init__()
        self.setupUi(self)
        BasePredictUi.__init__(self)

        self.output_dir = OUTPUT_DIR_CHANGHUA
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.now = QtCore.QDate.currentDate()
        self.lineEdit2.setText(self.now.toString('yyyy-MM-dd'))

        # 绑定按钮事件
        self.pushButton1.clicked.connect(self.import_folder)
        self.pushButton2.clicked.connect(self.folder_next)
        self.pushButton3.clicked.connect(self.folder_previous)
        self.pushButton4.clicked.connect(self.predict_jpg)
        self.pushButton5.clicked.connect(self.save_jpg)
        self.pushButton6.clicked.connect(self.go_init)
        self.pushButton7.clicked.connect(self.write_report)
        self.pushButton8.clicked.connect(self.close_dialog)

    @property
    def _model(self):
        return ModelManager().get_model('changhua')

    def predict_jpg(self):
        model = self._model
        if model is None:
            QMessageBox.warning(self, "提示", "模型尚未加载完成，请稍候...")
            return

        self.scores = [0 for _ in range(len(self.file_paths))]
        elapsed_time = len(self.file_paths)
        if elapsed_time == 0:
            QMessageBox.warning(self, "提示", "请先导入文件夹！")
            return

        self.pbar = QProgressDialog("诊断中", "取消", 0, elapsed_time, self)
        self.pbar.setWindowTitle("模型启动中")
        self.pbar.show()
        self.pbar.setValue(1)

        for flag, image_num in enumerate(self.file_paths):
            image = Image.open(image_num)
            _, img_name = os.path.split(image_num)
            predict_path = os.path.join(
                self.output_dir, img_name.replace(".jpg", ".png"))

            if not os.path.exists(predict_path):
                start = time.time()
                r_image, out_scores, out_classes, *_ = model.detect_image(image)
                elapsed = time.time() - start
                logger.debug("Changhua predict %.3fs for %s", elapsed, image_num)

                if out_scores.size != 0:
                    neo_scores = []
                    nonneo_scores = []
                    for i, cls in enumerate(out_classes):
                        if cls == 0:
                            neo_scores.append(out_scores[i])
                        elif cls == 1:
                            nonneo_scores.append(out_scores[i])
                    tempneo_max = round(max(neo_scores), 4) if neo_scores else 0
                    tempnonneo_max = round(max(nonneo_scores), 4) if nonneo_scores else 0
                    self.scores[flag] = max(tempneo_max, tempnonneo_max)

                r_image.save(predict_path)

            flag += 1
            self.pbar.setWindowTitle("检测进度")
            self.pbar.setValue(flag)
            QtCore.QCoreApplication.processEvents()
            if self.pbar.wasCanceled():
                break

        self.pbar.setValue(elapsed_time)
        QMessageBox.about(self, "提示", self.tr("图片检测完成"))


# ===================== OLGIM 综合评估模块 =====================
class OLGIMUi(QtWidgets.QMainWindow, OlgimUiForm, BasePredictUi):
    switch_init = QtCore.pyqtSignal()
    switch_info = QtCore.pyqtSignal()
    switch_gradcam = QtCore.pyqtSignal()

    def __init__(self):
        super(OLGIMUi, self).__init__()
        self.setupUi(self)
        BasePredictUi.__init__(self)

        self.output_dir = OUTPUT_DIR_OLGIM
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.now = QtCore.QDate.currentDate()
        self.lineEdit2.setText(self.now.toString('yyyy-MM-dd'))

        self.pushButton1.clicked.connect(self.import_folder)
        self.pushButton2.clicked.connect(self.folder_next)
        self.pushButton3.clicked.connect(self.folder_previous)
        self.pushButton4.clicked.connect(self.predict_jpg)
        self.pushButton5.clicked.connect(self.save_jpg)
        self.pushButton6.clicked.connect(self.go_init)
        self.pushButton7.clicked.connect(self.write_report)
        self.pushButton8.clicked.connect(self.close_dialog)
        self.pushButton9.clicked.connect(self.go_gradcam)

    @property
    def _model(self):
        return ModelManager().get_model('olgim')

    def go_gradcam(self):
        self.switch_gradcam.emit()

    def predict_jpg(self):
        model = self._model
        if model is None:
            QMessageBox.warning(self, "提示", "模型尚未加载完成，请稍候...")
            return

        self.scores = [0 for _ in range(len(self.file_paths))]
        elapsed_time = len(self.file_paths)
        if elapsed_time == 0:
            QMessageBox.warning(self, "提示", "请先导入文件夹！")
            return

        self.pbar = QProgressDialog("诊断中", "取消", 0, elapsed_time, self)
        self.pbar.setWindowTitle("模型启动中")
        self.pbar.show()
        self.pbar.setValue(1)

        for flag, image_num in enumerate(self.file_paths):
            image = Image.open(image_num)
            _, img_name = os.path.split(image_num)
            predict_path = os.path.join(
                self.output_dir, img_name.replace(".jpg", ".png"))

            if not os.path.exists(predict_path):
                r_image, out_scores, out_classes, *_ = model.detect_image(image)

                if out_scores.size != 0 and out_scores[0] > 0:
                    class0 = []
                    class2 = []
                    class3 = []
                    for i, cls in enumerate(out_classes):
                        if cls == 0:
                            class0.append(out_scores[i])
                        elif cls == 1:
                            class2.append(out_scores[i])
                        elif cls == 2:
                            class3.append(out_scores[i])
                    class0_max = round(max(class0), 6) if class0 else 0
                    class2_max = round(max(class2), 6) if class2 else 0
                    class3_max = round(max(class3), 6) if class3 else 0
                    self.scores[flag] = max(class0_max, class2_max, class3_max)

                r_image.save(predict_path)

            flag += 1
            self.pbar.setWindowTitle("检测进度")
            self.pbar.setValue(flag)
            QtCore.QCoreApplication.processEvents()
            if self.pbar.wasCanceled():
                break

        self.pbar.setValue(elapsed_time)
        QMessageBox.about(self, "提示", self.tr("图片检测完成"))
