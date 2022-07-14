"""
水平盒布局(QHBoxLayout)
"""

import sys,math
from PyQt5.QtWidgets import *

class HBoxLayout(QWidget):
    def __init__(self):
        super(HBoxLayout, self).__init__()
        self.setWindowTitle('水平盒布局')
        # 创建水平盒布局
        hlayout = QHBoxLayout()

        # 往布局里添加按钮控件
        hlayout.addWidget(QPushButton('按钮1'))
        hlayout.addWidget(QPushButton('按钮2'))
        hlayout.addWidget(QPushButton('按钮3'))
        hlayout.addWidget(QPushButton('按钮4'))
        hlayout.addWidget(QPushButton('按钮5'))

        # 此时按钮就会在水平方向等距的排列

        # 设置控件之间的间距
        hlayout.setSpacing(40)

        # 应用水平盒布局
        self.setLayout(hlayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = HBoxLayout()
    demo.show()
    sys.exit(app.exec_())
