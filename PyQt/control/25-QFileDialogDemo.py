"""
文件对话框 QFileDialog
最常用的是打开文件和保存文件对话框
"""
# 需求：
# 1.打开文件，显示到窗口上
# 2.打开文本文件，将文本文件的内容显示到窗口上

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QFileDialogDemo(QWidget):
    def __init__(self):
        super(QFileDialogDemo, self).__init__()
        self.initUI()

    # 编写初始化方法
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('文件对话框演示')

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建button1控件，用于加载图片
        self.button1 = QPushButton('加载图片')

        # 创建label控件，把图像显示到label控件上
        self.imageLabel = QLabel()

        # 创建button2控件，用于加载文件
        self.button2 = QPushButton('加载文本文件')

        # 创建QTextEdit控件，来显示文本加载的内容
        self.contents = QTextEdit('显示文本加载内容')

        # 连接信号槽
        self.button1.clicked.connect(self.loadImage)
        self.button2.clicked.connect(self.loadText)

        # 把控件添加到垂直布局里
        layout.addWidget(self.button1)
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.button2)
        layout.addWidget(self.contents)

        # 应用于垂直布局
        self.setLayout(layout)

    # 槽方法
    def loadImage(self):
        # 打开单个文件对话框
        # 下行代码第三个参数是默认路径，用 "."代替当前
        # 第四个参数：'图形文件 (*.jpg)'改成选中两种类型时有问题 '图形文件 (*.png,*.jpg)'
        # 弹出来的显示图片的窗口会随着图片尺寸大小的变化而变化
        fname,_ = QFileDialog.getOpenFileName(self,'打开文件','.','图形文件 (*.jpg)')
        # 得到图片文件名
        self.imageLabel.setPixmap(QPixmap(fname))
    def loadText(self):
        # 直接创建QFileDialog，第二种方法
        # 创建对象
        dialog = QFileDialog()
        # 设置文件创建模式
        dialog.setFileMode(QFileDialog.AnyFile)
        # 选择文件
        dialog.setFilter(QDir.Files)

        #打开文件
        if dialog.exec():
            # 如果打开成功
            filename = dialog.selectedFiles()
            # 打开文件，可以打开多个，取第一个
            f = open(filename[0],encoding='utf-8',mode='r')
            # 读取
            # 使用with的原因，自动关闭，当with读取结束后，会自动调用f里面的close方法关闭文档
            with f:
                data = f.read()
                self.contents.setText(data)


# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # app实例化，并传递参数
    app = QApplication(sys.argv)
    # 创建对象
    main = QFileDialogDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，通过exit函数
    sys.exit(app.exec_())
