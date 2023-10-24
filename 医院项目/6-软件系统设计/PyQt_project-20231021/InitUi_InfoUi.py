"""
    -*- coding: utf-8 -*-
    @Author: yaofanghao
    @Date: 2023/10/24 11:34
    @Filename: InitUi_InfoUi.py
    @Software: PyCharm     
"""
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog

# 导入需要的ui界面
from widgets.InitWidget import Ui_widget as init_Ui
from widgets.InfoWidget import Ui_Form as info_Ui


# 初始界面 InitWidget
class InitUi(QtWidgets.QMainWindow, init_Ui):
    switch_changhua = QtCore.pyqtSignal()
    switch_olgim = QtCore.pyqtSignal()

    def __init__(self):
        super(InitUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.go_changhua)  # 按下按钮1去肠化模块
        self.pushButton2.clicked.connect(self.go_olgim)  # 按下按钮2去OLGIM
        self.pushButton3.clicked.connect(self.close_dialog)   # 按下按钮3退出对话框

    def go_changhua(self):
        self.switch_changhua.emit()

    def go_olgim(self):
        self.switch_olgim.emit()

    def close_dialog(self):
        reply = QMessageBox.warning(self, "提示", "是否确定退出",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app_local = QtWidgets.QApplication.instance()
            app_local.quit()
        else:
            print('keep')


# 诊断报告填写 InfoWidget
class InfoUi(QtWidgets.QMainWindow, info_Ui):
    def __init__(self):
        super(InfoUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.save_info)  # 按下按钮1去保存信息
        self.pushButton2.clicked.connect(self.gen_report)  # 按下按钮2保存pdf
        self.pushButton3.clicked.connect(self.close_dialog)  # 关闭对话框
        self.output_pdf_dir = './img_out_report/'
        if not os.path.exists(self.output_pdf_dir):
            os.makedirs(self.output_pdf_dir)
        self.now = QtCore.QDate.currentDate()  # 获取当前日期
        self.lineEdit12.setText(self.now.toString('yyyy-MM-dd'))
        self.menzhenhao = self.lineEdit1.text()
        self.zhuyuanhao = self.lineEdit2.text()
        self.binglihao = self.lineEdit3.text()
        self.jianchahao = self.lineEdit4.text()
        self.name = self.lineEdit5.text()
        self.sex = self.lineEdit6.text()
        self.age = self.lineEdit7.text()
        self.ke = self.lineEdit8.text()
        self.chuang = self.lineEdit9.text()
        self.origin = self.lineEdit10.text()
        self.baogaoyishi = self.lineEdit11.text()
        self.chubuzhenduan = self.textEdit.toPlainText()
        print(self.chubuzhenduan)

    def close_dialog(self):
        reply = QMessageBox.warning(self, "提示", "是否确定退出",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app_local = QtWidgets.QApplication.instance()
            app_local.quit()
        else:
            print('keep')

    def save_info(self):
        print(self.textEdit.toPlainText())
        QMessageBox.about(self, "提示", self.tr("信息保存成功！"))

    def gen_report(self):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics  # 注册字体
        from reportlab.pdfbase.ttfonts import TTFont  # 字体类
        from reportlab.pdfgen import canvas  # 创建pdf文件
        # 1 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
        pdfmetrics.registerFont(TTFont('font1', os.getcwd()+str('\\pdf\\yangziti.ttf')))   # TTFont(字体名,字体文件路径)
        # 2.创建空白pdf文件
        filename, _ = QFileDialog.getSaveFileName(self, 'save file', self.output_pdf_dir, "ALL (*.pdf)")
        dst = os.path.join(self.output_pdf_dir, filename.replace(".jpg", ".pdf"))

        pdf_file = canvas.Canvas(dst, pagesize=A4)
        pdf_file.setFont("font1", 10)  # 设置字体和大小
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
            "    " + "检查号：" + str(jianchahao)
        )
        pdf_file.drawString(
            50, h - 100,
            "-----------------------------------------------------")
        pdf_file.drawString(
            50, h - 150,
            "姓名：" + str(name) +
            "    " + "性别：" + str(sex) +
            "    " + "年龄：" + str(age))
        pdf_file.drawString(
            50, h - 200,
            "科别：" + str(ke) +
            "    " + "床号：" + str(chuang) +
            "    " + "来源："+str(origin))
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
        pdf_file.drawString(
            50, h - 600, "日期：" + str(date))
        print(chubuzhenduan)

        pdf_file.save()
        QMessageBox.about(self, "提示", self.tr("报告保存成功！"))
