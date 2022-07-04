"""
颜色对话框 QColorDialog
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QColorDialogDemo(QWidget):
    def __init__(self):
        super(QColorDialogDemo, self).__init__()
        self.initUI()

    # 编写初始化方法
    def initUI(self):
        # 设置窗口标签
        self.setWindowTitle('选择颜色')

        # 创建布局
        layout = QVBoxLayout()
        # 创建button控件
        self.colorButton = QPushButton('选择颜色')
        # 创建label控件，用于设置接收颜色的输入框
        self.colorLabel = QLabel('Hello,测试颜色')

        # 创建Bgbutton控件，用来设置背景色
        self.colorBgButton = QPushButton('设置背景色')


        # 绑定信号 槽
        self.colorButton.clicked.connect(self.getColor)
        self.colorBgButton.clicked.connect(self.getBgColor)
        # 把控件放在布局里
        layout.addWidget(self.colorButton)
        layout.addWidget(self.colorLabel)
        layout.addWidget(self.colorBgButton)

        # 应用布局
        self.setLayout(layout)

    # 槽方法
    def getColor(self):
        # 返回color对象，探测是否点ok或者cancel
        # getColor返回一个值
        color = QColorDialog.getColor()
        # 设置文字颜色
        # 调色板实例化
        p =QPalette()
        p.setColor(QPalette.WindowText,color)
        # 设置调色板
        self.colorLabel.setPalette(p)
    # 背景色槽方法
    def getBgColor(self):
        color =  QColorDialog.getColor()
        # 调色板设置
        p = QPalette()
        p.setColor(QPalette.Window,color)
        # 设置自动填充
        self.colorLabel.setAutoFillBackground(True)
        # 设置调色板
        self.colorLabel.setPalette(p)

# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app = QApplication(sys.argv)
    # 把类实例化
    main = QColorDialogDemo()
    # 设置窗口
    main.show()
    # 进入程序的主循环，通过exit函数，确保主循环安全结束
    sys.exit(app.exec_())
