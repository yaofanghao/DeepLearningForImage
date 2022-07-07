"""
创建和使用状态栏

用于显示状态信息

"""
# 添加菜单 点击菜单会在状态栏里面显示五秒的信息，然后自动的消失
import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StatusBar(QMainWindow):
    def __init__(self):
        super(StatusBar, self).__init__()
        self.initUI()

    # 编写初始化的方法，规范代码
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('状态栏演示')
        # 设置尺寸
        self.resize(300,200)
        # 创建状态栏
        self.statusBar = QStatusBar()
        # 设置状态
        self.setStatusBar(self.statusBar)
        # 获得菜单栏
        bar = self.menuBar()
        # 在菜单栏里面添加"文件"菜单
        file = bar.addMenu("File")
        # 给文件菜单添加动作  给"文件"菜单添加子菜单
        file.addAction("show")
        # 添加触发的动作
        file.triggered.connect(self.processTrigger)


        # 放置一个中心控件
        self.setCentralWidget(QTextEdit())
    # 槽方法
    def processTrigger(self,q):
        if q.text() == "show":
            # 文本显示五秒钟，自动关闭
            self.statusBar.showMessage(q.text() + "菜单被点击了",5000)


# 防止别的脚本调用，只有单独执行此脚本时，才会调用下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = StatusBar()
    # 创建窗口
    main.show()
    # 执行主循环，调用exit方法，确保主循环安全退出
    sys.exit(app.exec_())
