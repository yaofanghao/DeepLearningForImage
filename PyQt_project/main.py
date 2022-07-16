# main函数功能：
# 实现各界面之间的跳转、交流
import sys
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsScene, QGraphicsPixmapItem
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

# AiqianWidget 癌前病变诊断界面
class AiqianUi(QtWidgets.QMainWindow, Aiqian_Ui):
    switch_init = QtCore.pyqtSignal()
    def __init__(self):
        super(AiqianUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.goInit)  # 按下按钮1去初始界面
        self.pushButton4.clicked.connect(self.getjpg)  # 按下按钮4读取图片
        self.pushButton6.clicked.connect(self.predictjpg) # 按下按钮6预测图片
        self.pushButton5.clicked.connect(self.closeDialog)  # 按下按钮5去关闭对话框
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
    def getjpg(self):
        global jpg_name # 图片设为全局变量，后续预测中也要用到
        jpg_name, imgType = QFileDialog.getOpenFileName(self, "选择图片", "./", "*.jpg;;*.png;;All Files(*)")
        print(jpg_name)
        if (jpg_name[0] == ""):
            QMessageBox.warning(self, "提示", self.tr("没有选择图片！"))
        else:
            print(jpg_name)
            # img = cv2.imread(image_path)  # 读取图像
            # imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
            # y, x = img.shape[:-1]
            # self.zoomscale = 1  # 图片放缩尺度
            # frame = QImage(imgrgb, x, y, QImage.Format_RGB888)
            # pix = QPixmap.fromImage(frame)
            # self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
            # self.item.setScale(self.zoomscale)
            # self.scene = QGraphicsScene()  # 创建场景
            # self.scene.clear()
            # # self.scene.addPixmap(self.pix)
            # # self.scene.addItem(self.item)
            # self.graphicsView.setScene(self.scene)
            # self.graphicsView.show()
            # print('success')
            #
            # 7.16 重写代码
            img = QPixmap(jpg_name).scaled(self.label5.width(), self.label5.height())
            self.label5.setPixmap(img)  # 显示读取图片到界面上
            self.lineEdit5.setText(jpg_name)
    def predictjpg(self):
        # 2022.7.16
        # 此为测试版的predict代码，测试qt能否成功运行
        # 后续根据实际需要全部修改替换
        import tensorflow as tf
        from PIL import Image
        from yolo_predict3 import YOLO

        gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        yolo = YOLO()
        while True:
            # img = input('Input image filename:')
            try:
                image = Image.open(jpg_name)
            except:
                print('Open Error! Try again!')
                continue
            else:
                r_image, out_scores, out_classes, top, right, left, bottom = yolo.detect_image(image)  # r_image 是预测生成图片
                # r_image.show()
                img_out = QPixmap(r_image).scaled(self.label6.width(), self.label6.height())
                self.label6.setPixmap(img_out)  # 显示预测图片到界面上

# EGCWidget 早癌EGC诊断系统界面
class EGCUi(QtWidgets.QMainWindow, EGC_Ui):
    switch_init = QtCore.pyqtSignal()
    def __init__(self):
        super(EGCUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.goInit)  # 按下按钮1去初始界面
        self.pushButton5.clicked.connect(self.closeDialog)  # 按下按钮5去关闭对话框
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
