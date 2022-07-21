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
        self.pushButton2.clicked.connect(self.saveInfo)  # 按下按钮2保存患者信息
        self.pushButton3.clicked.connect(self.chooseDialog)  # 按下按钮3去诊断系统选择框
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
        chubujiancha = self.textEdit.toPlainText()
        filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "./" ,'txt(*.txt)')
        print(filepath)
        with open(filepath,'w') as file: # 保存患者信息到txt
            file.write("门诊号："+str(menzhenhao))
            file.write('\r')
            file.write("住院号："+str(zhuyuanhao))
            file.write('\r')
            file.write("病历号："+str(binglihao))
            file.write('\r')
            file.write("检查号："+str(jianchahao))
            file.write('\r')
            file.write("姓名："+str(name))
            file.write('\r')
            file.write("性别："+str(sex))
            file.write('\r')
            file.write("年龄："+str(age))
            file.write('\r')
            file.write("科别："+str(ke))
            file.write('\r')
            file.write("床号："+str(chuang))
            file.write('\r')
            file.write("来源："+str(origin))
            file.write('\r')
            file.write("初步检查所见：\r"+str(chubujiancha))
            file.write("\r---------end---------")
            file.write('\r')

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

        self.pushButton1.clicked.connect(self.on_btnImportFolder_clicked) #导入文件夹
        self.pushButton2.clicked.connect(self.on_btnFolderNext_clicked) #下一个
        self.pushButton3.clicked.connect(self.on_btnFolderPrevious_clicked) #上一个
        self.pushButton4.clicked.connect(self.predictjpg) #开始检测

        self.pushButton6.clicked.connect(self.goInit)  # 去初始界面

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

    # 7.21
        # 导入文件夹
    # @pyqtSlot()
    def on_btnImportFolder_clicked(self):
        global cur_path  # 当前图片路径

        cur_dir = QtCore.QDir.currentPath()  # 获取当前文件夹路径
        # 选择文件夹
        dir_path = QFileDialog.getExistingDirectory(self, '打开文件夹', cur_dir)
        # 读取文件夹文件
        self.file_paths.clear()
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for file in files:
                self.file_paths.append(os.path.join(root, file))
        print(self.file_paths)
        if len(self.file_paths) <= 0:
            return
        # 获取第一个文件
        self.file_index = 0
        cur_path = self.file_paths[self.file_index]
        print(cur_path)
        img = QPixmap(cur_path).scaled(self.label5.width(), self.label5.height())
        self.label5.setPixmap(img)  # 显示读取图片到界面上
        self.lineEdit5.setText(cur_path)

    # 下一个文件
    # @pyqtSlot()
    def on_btnFolderNext_clicked(self):
        # 文件索引累加 1
        self.file_index += 1
        if self.file_index >= len(self.file_paths):
            QMessageBox.warning(self, "提示", self.tr("已经是最后一个！"))
            self.file_index = len(self.file_paths) - 1
        if len(self.file_paths) <= 0 or self.file_index >= len(self.file_paths):
            return
        cur_path = self.file_paths[self.file_index]
        print(cur_path)
        img = QPixmap(cur_path).scaled(self.label5.width(), self.label5.height())
        self.label5.setPixmap(img)  # 显示读取图片到界面上
        self.lineEdit5.setText(cur_path)

    # 上一个文件
    # @pyqtSlot()
    def on_btnFolderPrevious_clicked(self):
        # 文件索引减 1
        self.file_index -= 1
        if self.file_index < 0:
            QMessageBox.warning(self, "提示", self.tr("已经是第一个！"))
            self.file_index = 0
        if len(self.file_paths) <= 0 or self.file_index >= len(self.file_paths):
            return
        # 当前路径
        cur_path = self.file_paths[self.file_index]
        print(cur_path)
        img = QPixmap(cur_path).scaled(self.label5.width(), self.label5.height())
        self.label5.setPixmap(img)  # 显示读取图片到界面上
        self.lineEdit5.setText(cur_path)

    def predictjpg(self):
        # 2022.7.16
        # 此为测试版的predict代码，测试qt能否成功运行
        # 后续根据实际需要全部修改替换
        import tensorflow as tf
        from PIL import Image
        from yolo_predict3 import YOLO

        # 进度条
        elapsed_time = 100000
        self.pbar = QProgressDialog("诊断中", "取消", 0, elapsed_time, self)
        self.pbar.setWindowTitle("进度提示")
        self.pbar.show()

        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        yolo = YOLO()
        while True:
            try:
                image = Image.open(self.file_paths[self.file_index])
            except:
                print('Open Error! Try again!')
                continue
            else:
                for i in range(elapsed_time):  # 进度条显示进度
                    self.pbar.setValue(i)
                    QtCore.QCoreApplication.processEvents()
                    if self.pbar.wasCanceled():
                        break
                r_image, out_scores, out_classes, top, right, left, bottom = yolo.detect_image(image)  # r_image 是预测生成图片
                # 目前实现的办法：先保存再读取
                r_image.save(self.file_paths[self.file_index].replace(".jpg", ".png"))
                img_out = QPixmap(self.file_paths[self.file_index].replace(".jpg", ".png")).scaled(self.label6.width(),self.label6.height())
                self.label6.setPixmap(img_out)  # 显示预测图片到界面上

                self.pbar.setValue(elapsed_time) # 进度条加满

                break

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
