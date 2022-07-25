# main函数功能：
# 实现各界面之间的跳转、交流
import sys
import cv2
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QProgressDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage

# 导入需要的ui界面
from InitWidget import Ui_widget as Init_Ui
from InfoWidget import Ui_Form as Info_Ui
from AiqianWidget import Ui_Form as Aiqian_Ui
from EGCWidget import Ui_Form as EGC_Ui

# 初始界面 InitWidget
class InitUi(QtWidgets.QMainWindow, Init_Ui):
    switch_info = QtCore.pyqtSignal()
    def __init__(self):
        super(InitUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.goInfo)  # 按下按钮1去患者信息界面
        self.pushButton2.clicked.connect(self.goInfo)  # 按下按钮2去患者信息界面
        self.pushButton5.clicked.connect(self.closeDialog)   # 按下按钮5去退出对话框
    def goInfo(self):
        self.switch_info.emit()
    def closeDialog(self):
        reply = QMessageBox.warning(self,"提示","是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
        else:
            print('keep')

# 患者信息界面 InfoWidget
class InfoUi(QtWidgets.QMainWindow, Info_Ui):
    switch_init = QtCore.pyqtSignal()
    switch_aiqian = QtCore.pyqtSignal()
    switch_egc = QtCore.pyqtSignal()
    def __init__(self):
        super(InfoUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.goInit)  # 按下按钮1去初始界面
        self.pushButton2.clicked.connect(self.saveInfo)  # 按下按钮2确认保存信息，用于后续报告生成
        self.pushButton3.clicked.connect(self.chooseDialog)  # 按下按钮3去诊断系统选择框
        # 因为下面这些信息后续生成报告要用到，所以在这里添加值，方便别的类调用
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
        self.chubujiancha = self.textEdit.toPlainText()
    def goInit(self):
        self.switch_init.emit()
    def chooseDialog(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        panel = QLabel()
        panel.setText("请确认您要选择的诊断系统")
        self.dialog = QDialog()
        self.aiqianButton = QPushButton("癌前病变诊断")
        self.egcButton = QPushButton("早癌EGC诊断")
        self.aiqianButton.clicked.connect(self.goAiqian)
        self.egcButton.clicked.connect(self.goEGC)
        self.dialog.setWindowTitle("开始内镜检测")
        hbox.addWidget(self.aiqianButton)
        hbox.addWidget(self.egcButton)
        vbox.addWidget(panel)
        vbox.addLayout(hbox)
        self.dialog.setLayout(vbox)
        self.dialog.setWindowModality(QtCore.Qt.ApplicationModal)  # 该模式下，只有该dialog关闭，才可以关闭父界面
        self.dialog.exec_()
    def goAiqian(self):
        self.switch_aiqian.emit()
        self.dialog.close()
    def goEGC(self):
        self.switch_egc.emit()
        self.dialog.close()
    def saveInfo(self):
        QMessageBox.about(self, "提示", self.tr("信息保存成功！"))

# AiqianWidget 癌前病变诊断界面
class AiqianUi(QtWidgets.QMainWindow, Aiqian_Ui):
    switch_init = QtCore.pyqtSignal()
    def __init__(self):
        super(AiqianUi, self).__init__()
        self.setupUi(self)
        self.pushButton6.clicked.connect(self.goInit)  # 去初始界面
        self.pushButton8.clicked.connect(self.closeDialog)  # 关闭对话框
    def goInit(self):
        self.switch_init.emit()
    def closeDialog(self):
        reply = QMessageBox.warning(self,"提示","是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
        else:
            print('keep')

# EGCWidget 早癌EGC诊断系统界面
class EGCUi(QtWidgets.QMainWindow, EGC_Ui):
    switch_init = QtCore.pyqtSignal()
    def __init__(self):
        super(EGCUi, self).__init__()
        self.setupUi(self)

        self.file_paths = []  # 文件列表
        self.file_index = 0	  # 文件索引
        self.scores = []  # 置信度分数列表


        self.output_dir = './img_out/'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_pdf_dir = './img_out_report/'
        if not os.path.exists(self.output_pdf_dir):
            os.makedirs(self.output_pdf_dir)

        self.now = QtCore.QDate.currentDate()  # 获取当前日期
        self.lineEdit2.setText(self.now.toString(QtCore.Qt.ISODate))  # 显示时间到界面
        self.pushButton1.clicked.connect(self.on_btnImportFolder_clicked)  # 导入文件夹
        self.pushButton2.clicked.connect(self.on_btnFolderNext_clicked)  # 下一个
        self.pushButton3.clicked.connect(self.on_btnFolderPrevious_clicked)  # 上一个
        self.pushButton4.clicked.connect(self.predictJpg)  # 开始检测
        self.pushButton5.clicked.connect(self.saveJpg)  # 显示并保存图片
        self.pushButton6.clicked.connect(self.goInit)  # 去初始界面
        self.pushButton7.clicked.connect(self.saveReport)  # 生成pdf报告
        self.pushButton8.clicked.connect(self.closeDialog)  # 关闭对话框
    def goInit(self):
        self.switch_init.emit()
    def closeDialog(self):  # 导入文件夹
        reply = QMessageBox.warning(self, "提示", "是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
        else:
            print('keep')
    def on_btnImportFolder_clicked(self):
        cur_dir = QtCore.QDir.currentPath()  # 获取当前文件夹路径
        # 选择文件夹
        dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹', cur_dir)
        # 读取文件夹文件
        self.file_paths.clear()
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:
                self.file_paths.append(os.path.join(root, file))
        if len(self.file_paths) <= 0:
            return
        self.file_index = 0  # 获取第一个文件
        cur_path = self.file_paths[self.file_index]
        filepath, filename = os.path.split(cur_path)  # 分离文件路径和名称
        img = QPixmap(cur_path).scaled(self.label5.width(), self.label5.height())
        self.label5.setPixmap(img)  # 显示读取图片到界面上
        self.lineEdit5.setText(filename)
    def on_btnFolderNext_clicked(self):  # 下一个文件
        self.file_index += 1  # 文件索引累加 1
        if self.file_index >= len(self.file_paths):
            QMessageBox.warning(self, "提示", self.tr("已经是最后一个！"))
            self.file_index = len(self.file_paths) - 1
        if len(self.file_paths) <= 0 or self.file_index >= len(self.file_paths):
            return
        cur_path = self.file_paths[self.file_index]
        filepath, filename = os.path.split(cur_path)  # 分离文件路径和名称
        img = QPixmap(cur_path).scaled(self.label5.width(), self.label5.height())
        self.label5.setPixmap(img)  # 显示读取图片到界面上
        self.lineEdit5.setText(filename)
        img_out = QPixmap(os.path.join(self.output_dir,filename.replace(".jpg", ".png"))).scaled(self.label6.width(), self.label6.height())
        self.label6.setPixmap(img_out)  # 显示预测图片到界面上
    def on_btnFolderPrevious_clicked(self):  # 下一个文件
        self.file_index -= 1  # 文件索引减 1
        if self.file_index < 0:
            QMessageBox.warning(self, "提示", self.tr("已经是第一个！"))
            self.file_index = 0
        if len(self.file_paths) <= 0 or self.file_index >= len(self.file_paths):
            return
        cur_path = self.file_paths[self.file_index]
        filepath, filename = os.path.split(cur_path)  # 分离文件路径和名称
        img = QPixmap(cur_path).scaled(self.label5.width(), self.label5.height())
        self.label5.setPixmap(img)  # 显示读取图片到界面上
        self.lineEdit5.setText(filename)
        img_out = QPixmap(os.path.join(self.output_dir,filename.replace(".jpg", ".png"))).scaled(self.label6.width(), self.label6.height())
        self.label6.setPixmap(img_out)  # 显示预测图片到界面上

    def predictJpg(self):
        # 2022.7.16
        # 此为测试版的predict代码，测试能否成功运行
        # 后续根据实际需要全部修改替换
        import tensorflow as tf
        from PIL import Image
        from predict11 import predict11_single
        # from yolo_predict3 import YOLO
        # 进度条
        elapsed_time = len(self.file_paths)  # 进度条按比例划分为图片个数
        self.pbar = QProgressDialog("诊断中", "取消", 0, elapsed_time, self)
        self.pbar.setWindowTitle("进度提示")
        self.pbar.show()
        self.pbar.setValue(0)

        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        flag = 0
        for image_num in self.file_paths:
            image = Image.open(image_num)
            print(image_num)

            # 关键部分！返回新的画框图和新的置信度，并实现了分类至NEO\NONNEO等：
            r_image, new_scores = predict11_single(image, image_num)
            self.scores.append(new_scores)  # 把每张图置信度结果存放至scores列表中
            print('success')

            # 目前实现的办法：先保存再读取
            # cur_path = self.file_paths[self.file_index]
            filepath, filename = os.path.split(image_num)  # 分离文件路径和名称
            dst = os.path.join(self.output_dir,filename.replace(".jpg", ".png"))
            r_image.save(dst)  # 保存预测图片至img_out
            flag += 1
            self.pbar.setValue(flag) # 进度条每处理完一张图片加一份
            QtCore.QCoreApplication.processEvents()
            if self.pbar.wasCanceled():
                break

        self.pbar.setValue(elapsed_time) # 进度条加满
        # break
        QMessageBox.about(self, "提示", self.tr("图片检测完成"))

    def saveJpg(self):  # 显示图片
        cur_path = self.file_paths[self.file_index]
        filepath, filename = os.path.split(cur_path)  # 分离文件路径和名称
        img_out = QPixmap(os.path.join(self.output_dir,filename.replace(".jpg", ".png"))).scaled(self.label6.width(), self.label6.height())
        self.label6.setPixmap(img_out)  # 显示预测图片到界面上
        print(self.file_index)
        print(self.scores)
        self.lineEdit3.setText(str(self.scores[self.file_index]))  # 显示置信度分数到界面上
        QMessageBox.about(self, "提示", self.tr("图片已保存，分类至NEO和NONNEO文件夹！"))

    def saveReport(self):
        from reportlab.pdfbase import pdfmetrics  # 注册字体
        from reportlab.pdfbase.ttfonts import TTFont  # 字体类
        from reportlab.pdfgen import canvas  # 创建pdf文件
        # 7.22 未完成
        cur_path = self.file_paths[self.file_index]
        filepath, filename = os.path.split(cur_path)  # 分离文件路径和名称
        # 1 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
        pdfmetrics.registerFont(TTFont('font1', os.getcwd()+str('\\pdf\\yangziti.ttf')))   # TTFont(字体名,字体文件路径)
        #2.创建空白pdf文件
        dst = os.path.join(self.output_pdf_dir, filename.replace(".jpg", ".pdf"))
        pdf_file = canvas.Canvas(dst)
        #3.写字体
        pdf_file.setFont("yang",40)  #设置字体
        #设置文字颜色
        # r g b 范围（0（0）-1（255） ）  最后透明度
        pdf_file.setFillColorRGB(1,0,0,1)
        # 渲染文字
        pdf_file.drawString(100,100,"yang")

        #保存
        pdf_file.save()
        QMessageBox.about(self, "提示", self.tr("报告保存成功！"))

# 控制器，实现各界面之间的跳转功能
class Controller:
    def __init__(self):
        pass
        # 对各窗口实例化
        self.initUi = InitUi()
        self.info = InfoUi()
        self.aiqian = AiqianUi()
        self.egc = EGCUi()

    def showInit(self):
        self.initUi.switch_info.connect(self.showInfo)
        self.info.close()
        self.aiqian.close()
        self.egc.close()
        self.initUi.show()
    def showInfo(self):
        self.info.switch_init.connect(self.showInit)
        self.info.switch_aiqian.connect(self.showAiqian)
        self.info.switch_egc.connect(self.showEGC)
        self.initUi.close()
        self.info.show()
    def showAiqian(self):
        self.aiqian.switch_init.connect(self.showInit)
        self.initUi.close()
        self.info.close()
        self.aiqian.show()
    def showEGC(self):
        self.egc.switch_init.connect(self.showInit)
        self.initUi.close()
        self.info.close()
        self.egc.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    controller = Controller()
    controller.showInit()  # 启动初始界面为InitWidget

    sys.exit(app.exec_())
