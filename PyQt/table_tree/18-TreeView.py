"""
QTreeView控件与系统定制模式

与QTreeWidget的不同点： QTreeWiget装载数据的方式是通过Model,比如Model里面的QDirModel 用来显示当前操作系统的目录结构
QTreeView  一般用于比较复杂的树
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建QDirModel控件
    model = QDirModel()
    # 创建QTreeView控件
    tree = QTreeView()
    # 设置model
    tree.setModel(model)

    # 把树作为一个窗口
    tree.setWindowTitle('QTreeView')
    # 设置树窗口的尺寸
    tree.resize(600,400)
    # 显示树
    tree.show()
    sys.exit(app.exec_())


