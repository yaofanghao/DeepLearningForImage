# main函数功能：
# 实现各界面之间的跳转、交流
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys

# 导入需要的ui界面
from InitWidget import Ui_Form as Init_Ui
from InfoWidget import Ui_Form as Info_Ui
from AiqianWidget import Ui_Form as Aiqian_Ui
from EGCWidget import Ui_Form as EGC_Ui

# 初始界面 InitWidget
class InitUi(QtWidgets.QMainWindow, Init_Ui):
    switch_aiqian = QtCore.pyqtSignal()  # 跳转至癌前诊断界面的信号
    switch_egc = QtCore.pyqtSignal()  # 跳转至早癌诊断界面的信号
    def __init__(self):
        super(InitUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.goAiqian) # 按下按钮1去癌前诊断界面
        self.pushButton2.clicked.connect(self.goEGC) # 按下按钮2去早癌诊断界面
        self.pushButton5.clicked.connect(self.closeEvent)  # 按下按钮3去关闭对话框
    def goAiqian(self):
        self.switch_aiqian.emit()
    def goEGC(self):
        self.switch_egc.emit()
    def closeEvent(self):
        reply = QMessageBox.warning(self,"提示","是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
            # event.accept()
        else:
            print('keep')
            # event.ignore()

# 患者信息界面 InfoWidget
class InfoUi(QtWidgets.QMainWindow, Info_Ui):
    def __init__(self):
        super(InfoUi, self).__init__()
        self.setupUi(self)

# AiqianWidget 癌前病变诊断界面
class AiqianUi(QtWidgets.QMainWindow, Aiqian_Ui):
    switch_init = QtCore.pyqtSignal()
    def __init__(self):
        super(AiqianUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.goInit) # 按下按钮1去初始界面
        self.pushButton5.clicked.connect(self.closeEvent) # 按下按钮5去关闭对话框
    def goInit(self):
        self.switch_init.emit()
    def closeEvent(self):
        reply = QMessageBox.warning(self,"提示","是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
            # event.accept()
        else:
            print('keep')
            # event.ignore()

# EGCWidget 早癌EGC诊断系统界面
class EGCUi(QtWidgets.QMainWindow, EGC_Ui):
    switch_init = QtCore.pyqtSignal()
    def __init__(self):
        super(EGCUi, self).__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.goInit) # 按下按钮1去初始界面
        self.pushButton5.clicked.connect(self.closeEvent) # 按下按钮5去关闭对话框
    def goInit(self):
        self.switch_init.emit()
    def closeEvent(self):
        reply = QMessageBox.warning(self,"提示","是否确定退出",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('exit')
            app = QtWidgets.QApplication.instance()
            app.quit()
            # event.accept()
        else:
            print('keep')
            # event.ignore()

# 控制器，实现各界面之间的跳转功能
class Controller:
    def __init__(self):
        pass
    def showInit(self): # 在InitWidget中，按下不同按钮进入不同预测界面
        self.initUi = InitUi()
        self.initUi.switch_aiqian.connect(self.showAiqian)
        self.initUi.switch_egc.connect(self.showEGC)
        self.initUi.show()
    def showAiqian(self):
        self.aiqian = AiqianUi()
        self.aiqian.switch_init.connect(self.showInit)
        self.initUi.close()
        self.aiqian.show()
    def showEGC(self):
        self.egc = EGCUi()
        self.egc.switch_init.connect(self.showInit)
        self.initUi.close()
        self.egc.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    controller = Controller()
    controller.showInit()  # 启动初始界面为InitWidget


    sys.exit(app.exec_())
