"""
容纳多文档的窗口

QMdiArea  容纳多文档类
QMdiSubWindow  多文档窗口类

# 父窗口可以创建多个子窗口，子窗口不能离开父窗口
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MultiWindows(QMainWindow):
    # 记录一下当前的窗口
    count = 0
    def __init__(self,parent=None):
        super(MultiWindows, self).__init__(parent)

        self.setWindowTitle("容纳多文档的窗口")
        # 多文档有两种排列方式 一种是平铺，一种是层叠
        # 创建容纳多文档对象
        self.mdi = QMdiArea()
        # 把多文档对象添加到布局里面
        self.setCentralWidget(self.mdi)
        # 创建一个菜单
        bar = self.menuBar()
        # 添加一个文件菜单
        file = bar.addMenu("File")
        # 给文件菜单添加动作 "New"
        file.addAction("New")
        # 设置窗口的排列方式
        # 层叠
        file.addAction("cascade")
        # 平铺
        file.addAction("Tiled")
        # 连接菜单动作，触发信号
        file.triggered.connect(self.windowaction)

    # 槽方法
    def windowaction(self,q):
        print(q.text())
        # q 是当前单击的菜单项
        if q.text() == "New":
            # 记录一下
            MultiWindows.count = MultiWindows.count + 1
            # 创建一个子窗口
            sub = QMdiSubWindow()
            # 在子窗口里面放置控件
            sub.setWidget(QTextEdit())
            # 设置子窗口的标题
            sub.setWindowTitle('子窗口' + str(MultiWindows.count))
            # 添加子窗口
            self.mdi.addSubWindow(sub)
            # 显示子窗口
            sub.show()
        elif q.text() == "cascade":
            # 设置层叠方式
            self.mdi.cascadeSubWindows()
        elif q.text() == "Tiled":
            # 设置平铺方式
            self.mdi.tileSubWindows()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MultiWindows()
    demo.show()
    sys.exit(app.exec_())
