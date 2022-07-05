"""
让控件支持拖拽动作
如果把A拖到B
A.setDragEnabled(True)   让A可以拖动
B.setAcceptDrops(True)   让B可以接收其他控件
B需要两个事件
1.dragEnterEvent    将A拖到B触发
2.dropEvent         在B的区域放下A时触发
"""
# demo:将一个文本输入框里面的文字拖到一个QChickBox控件里面，(把文字追加到QChickBox里面)

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# B
# QComboBox 下拉框
class MyComboBox(QComboBox):
    def __init__(self):
        super(MyComboBox, self).__init__()
        # 把这个控件SetAcceptDrops为True,就可以接收别的控件了
        self.setAcceptDrops(True)
    # 别的控件拖进来，还没松鼠标，还没触发
    def dragEnterEvent(self, e):
        print(e)
        # 查看接收的文本，如果有文本，进行处理
        if e.mimeDate().hasText():
            e.accept()
        else:
            e.ignore()
    # 把别的控件拖进来放下
    def dropEvent(self, e):
        # self指当前下拉列表控件
        # 得到一个文本输入框的文本
        self.addItem(e.mimeDate().text())


# A
class DrapDropDemo(QWidget):
    def __init__(self):
        super(DrapDropDemo, self).__init__()
        # 创建一个form表单布局
        formLayout = QFormLayout()
        # 把控件添加到布局里
        formLayout.addRow(QLabel("请将左边的文本拖拽到右边的下拉列表中"))
        # 创建文本输入框  在左侧显示
        lineEdit = QLineEdit()
        # 被拖动的控件设置可以拖动  让QLineEdit控件可拖动
        lineEdit.setDragEnabled(True)
        # 创建下拉列表控件
        combo = MyComboBox()
        # 把控件添加到form布局里  左侧为lineEdit ,右侧为下拉列表控件
        formLayout.addRow(lineEdit,combo)
        # 应用于布局
        self.setLayout(formLayout)
        # 设置标题
        self.setWindowTitle('拖拽案例')

# 防止别脚本调用，只有直接运行此脚本，才会执行下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = DrapDropDemo()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，让主循环安全退出
    sys.exit(app.exec_())
