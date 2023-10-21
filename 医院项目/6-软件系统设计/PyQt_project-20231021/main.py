# main函数功能：
# 实现各界面之间的跳转、交流
import sys
import numpy
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QProgressDialog
from PyQt5.QtGui import QPixmap

# 导入需要的ui界面
from InitWidget import Ui_widget as Init_Ui
from InfoWidget import Ui_Form as Info_Ui
from OLGIMWidget import Ui_Form as OLGIM_ui

# 导入faster-RCNN模型类
from frcnn import FRCNN
frcnn = FRCNN()
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)

# 初始界面 InitWidget
class InitUi(QtWidgets.QMainWindow, Init_Ui):
    switch_olgim = QtCore.pyqtSignal()

    def __init__(self):
        super(InitUi, self).__init__()
        self.setupUi(self)
        self.pushButton2.clicked.connect(self.goOlgim)  # 按下按钮2去OLGIM
        self.pushButton3.clicked.connect(self.closeDialog)   # 按下按钮3退出对话框

    def goOlgim(self):
        self.switch_olgim.emit()

    def closeDialog(self):
        reply = QMessageBox.warning(self,"提示","是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
        else:
            print('keep')

# OLGIMUi OLGIM综合评估模型界面
class OLGIMUi(QtWidgets.QMainWindow, OLGIM_ui):
    switch_init = QtCore.pyqtSignal()
    switch_info = QtCore.pyqtSignal()
    def __init__(self):
        super(OLGIMUi, self).__init__()
        self.pbar = None
        self.setupUi(self)

        self.file_paths = []  # 文件列表
        self.file_index = 0	  # 文件索引

        self.output_dir = './img_out/'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.now = QtCore.QDate.currentDate()  # 获取当前日期
        self.lineEdit2.setText(self.now.toString(QtCore.Qt.ISODate))  # 显示时间到界面
        self.pushButton1.clicked.connect(self.on_btnImportFolder_clicked)  # 导入文件夹
        self.pushButton2.clicked.connect(self.on_btnFolderNext_clicked)  # 下一个
        self.pushButton3.clicked.connect(self.on_btnFolderPrevious_clicked)  # 上一个
        self.pushButton4.clicked.connect(self.predictJpg)  # 开始检测
        self.pushButton5.clicked.connect(self.saveJpg)  # 显示并保存图片
        self.pushButton6.clicked.connect(self.goInit)  # 去初始界面
        self.pushButton7.clicked.connect(self.writeReport)  # 去填写报告界面
        self.pushButton8.clicked.connect(self.closeDialog)  # 关闭对话框
    def goInit(self):
        self.switch_init.emit()
    def closeDialog(self):
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
        self.scores = [0 for _ in range(len(self.file_paths))]  # 创建置信度分数列表，暂时全为0
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
        self.lineEdit3.setText(str(self.scores[self.file_index]))  # 显示置信度分数到界面上
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
        self.lineEdit3.setText(str(self.scores[self.file_index]))  # 显示置信度分数到界面上
        img_out = QPixmap(os.path.join(self.output_dir,filename.replace(".jpg", ".png"))).scaled(self.label6.width(), self.label6.height())
        self.label6.setPixmap(img_out)  # 显示预测图片到界面上
    def predictJpg(self):
        # 此为测试版的predict代码，测试能否成功运行
        # 后续根据实际需要全部修改替换

        from PIL import Image

        # 进度条
        elapsed_time = len(self.file_paths)  # 进度条按比例划分为图片个数
        self.pbar = QProgressDialog("诊断中", "取消", 0, elapsed_time, self)
        self.pbar.setWindowTitle("进度提示")
        self.pbar.show()
        self.pbar.setValue(1)

        flag = 0
        for image_num in self.file_paths:
            image = Image.open(image_num)
            print(image_num)

            # 如果img_out文件夹中已经存在预测图片，跳过以下步骤
            _, img_name = os.path.split(image_num)
            if not os.path.exists(os.path.join('./img_out/', img_name)):

                # 关键部分！返回新的画框图和新的置信度，并实现了分类至0-1分\2分\3分等：
                r_image, out_scores, out_classes, top, right, left, bottom = frcnn.detect_image(image)

                print("success predict!")

                if out_scores[0] == 0:  # 2023.3.2 解决了部分图片non-iterale的错误问题
                    self.scores[flag] = 0

                if (out_scores.size != 0) & (out_scores[0] > 0):
                    ################ 找到置信度最大的类别的算法 ############
                    num = 0
                    t = out_scores
                    class0 = numpy.array([0])
                    class2 = numpy.array([0])
                    class3 = numpy.array([0])

                    for i in out_classes:
                        if i == 0:  # 0-1分
                            class0 = numpy.append(class0, t[num])
                        if i == 1:  # 2分
                            class2 = numpy.append(class2, t[num])
                        if i == 2:  # 3分
                            class3 = numpy.append(class3, t[num])
                        num += 1

                    # 得到各类别分数的最大值 非常重要！
                    class0_max = numpy.max(class0)
                    class0_max = round(class0_max, 6)
                    class2_max = numpy.max(class2)
                    class2_max = round(class2_max, 6)
                    class3_max = numpy.max(class3)
                    class3_max = round(class3_max, 6)

                    max_output = max(class0_max, class2_max, class3_max)
                    self.scores[flag] = max_output  # 把每张图置信度结果存放至scores列表中

                # 目前实现的办法：先保存再读取
                # cur_path = self.file_paths[self.file_index]
                filepath, filename = os.path.split(image_num)  # 分离文件路径和名称
                dst = os.path.join(self.output_dir,filename.replace(".jpg", ".png"))
                r_image.save(dst)  # 保存预测图片至img_out
                print('success save!')

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
        QMessageBox.about(self, "提示", self.tr("图片已保存，分类至指定文件夹！"))
    def writeReport(self):
        self.switch_info.emit()  # 进入报告填写界面InfoWidget

# 诊断报告填写 InfoWidget
class InfoUi(QtWidgets.QMainWindow, Info_Ui):
    def __init__(self):
        super(InfoUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.saveInfo)  # 按下按钮1去保存信息
        self.pushButton2.clicked.connect(self.genReport)  # 按下按钮2保存pdf
        self.pushButton3.clicked.connect(self.closeDialog)  # 关闭对话框
        self.output_pdf_dir = './img_out_report/'
        if not os.path.exists(self.output_pdf_dir):
            os.makedirs(self.output_pdf_dir)

        self.now = QtCore.QDate.currentDate()  # 获取当前日期
        self.lineEdit12.setText(self.now.toString(QtCore.Qt.ISODate))
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
    def closeDialog(self):
        reply = QMessageBox.warning(self, "提示", "是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
        else:
            print('keep')
    def saveInfo(self):
        print(self.textEdit.toPlainText())
        QMessageBox.about(self, "提示", self.tr("信息保存成功！"))

    def genReport(self):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfbase import pdfmetrics  # 注册字体
        from reportlab.pdfbase.ttfonts import TTFont  # 字体类
        from reportlab.pdfgen import canvas  # 创建pdf文件
        # 1 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)
        pdfmetrics.registerFont(TTFont('font1', os.getcwd()+str('\\pdf\\yangziti.ttf')))   # TTFont(字体名,字体文件路径)
        #2.创建空白pdf文件
        self.filename, type = QFileDialog.getSaveFileName(self,'save file',self.output_pdf_dir, "ALL (*.pdf)")
        dst = os.path.join(self.output_pdf_dir, self.filename.replace(".jpg", ".pdf"))

        pdf_file = canvas.Canvas(dst,pagesize=A4)
        pdf_file.setFont("font1",20)  #设置字体和大小
        pdf_file.setFillColorRGB(0,0,0,1)
        w,h = A4

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

        pdf_file.drawString(50, h - 50, "门诊号："+str(menzhenhao)+"    "+"住院号："+str(zhuyuanhao)+\
                            "    "+"病历号：" + str(binglihao)+"    "+"检查号：" + str(jianchahao))
        pdf_file.drawString(50, h - 100, "-----------------------------------------------------")
        pdf_file.drawString(50, h - 150, "姓名：" + str(name)+"    "+ "性别：" + str(sex)+\
                            "    "+"年龄：" + str(age))
        pdf_file.drawString(50, h - 200, "科别：" + str(ke)+"    "+ "床号：" + str(chuang)+\
                            "    "+"来源：" + str(origin))
        pdf_file.drawString(50, h - 250, "-----------------------------------------------------")
        pdf_file.drawString(50, h - 300,"初步诊断所见："+str(chubuzhenduan))
        pdf_file.drawString(50, h - 500, "-----------------------------------------------------")
        pdf_file.drawString(50, h - 550,"报告医师：" + str(baogaoyishi))
        pdf_file.drawString(50, h - 600, "日期："+str(date))
        print(chubuzhenduan)

        pdf_file.save()

        QMessageBox.about(self, "提示", self.tr("报告保存成功！"))


# 控制器，实现各界面之间的跳转功能
class Controller:
    def __init__(self):
        # 对各窗口实例化
        self.initUi = InitUi()
        self.olgim = OLGIMUi()
        self.info = InfoUi()

    def showInit(self):
        self.initUi.switch_olgim.connect(self.showOLGIM)
        self.info.close()
        self.olgim.close()
        self.initUi.show()
    def showInfo(self):
        self.initUi.close()
        # self.olgim.close()
        self.info.show()

    def showOLGIM(self):
        self.olgim.switch_init.connect(self.showInit)
        self.olgim.switch_info.connect(self.showInfo)
        self.initUi.close()
        self.info.close()
        self.olgim.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    controller = Controller()
    controller.showInit()  # 启动初始界面为InitWidget

    # w = QtWidgets.QWidget()
    #
    # ui = main2.Test()
    #
    # ui.setUI(w)

    sys.exit(app.exec_())
