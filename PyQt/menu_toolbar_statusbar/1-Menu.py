"""
创建和使用菜单
"""

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Menu(QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()

        # 设置窗口尺寸
        self.resize(300,200)
        # 获取菜单栏
        bar = self.menuBar()

        # 给菜单栏添加 "文件"
        file = bar.addMenu("文件")
        # 给文件添加动作 "新建"
        # 第一种添加方式
        file.addAction("新建")


        # 第二种添加方式  通过QAction
        # 添加动作 "保存"
        save = QAction("保存",self)
        # 给保存添加快捷键
        save.setShortcut("Ctrl + S")
        # 把"保存"动作添加到"文件"下面
        file.addAction(save)

        # 把save触发连接槽
        save.triggered.connect(self.process)

        # 给菜单栏添加"编辑"菜单
        edit = bar.addMenu("Edit")
        # 给"编辑"添加"复制"动作
        edit.addAction("copy")
        # 给"编辑"添加"粘贴"动作
        edit.addAction("paste")
        # 创建"退出"动作
        quit =QAction("Quit",self)
        # 把"退出"添加到"文件"下面
        file.addAction(quit)


    # 给动作添加事件
    def process(self,a):
        print(self.sender().text())

# 直接运行此脚本，才会调用下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app =   QApplication(sys.argv)
    # 创建对象
    main = Menu()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，确保主循环安全退出
    sys.exit(app.exec_())
