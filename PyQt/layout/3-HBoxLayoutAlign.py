"""
设置控件的对齐方式

左对齐  右对齐  顶端对齐  底端对齐
"""

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class HBoxLayoutAlign(QWidget):
    def __init__(self):
        super(HBoxLayoutAlign, self).__init__()
        self.setWindowTitle('设置控件的对齐方式')
        # 创建水平盒布局
        hlayout = QHBoxLayout()

        # 往布局里添加按钮控件

        # 按钮1设置左对齐 顶端对齐
        hlayout.addWidget(QPushButton('按钮1'),1,Qt.AlignLeft | Qt.AlignTop)
        hlayout.addWidget(QPushButton('按钮2'),2,Qt.AlignLeft | Qt.AlignTop)
        hlayout.addWidget(QPushButton('按钮3'))
        hlayout.addWidget(QPushButton('按钮4'),1,Qt.AlignLeft | Qt.AlignBottom)
        hlayout.addWidget(QPushButton('按钮5'),1,Qt.AlignLeft | Qt.AlignBottom)

        # 此时按钮就会在水平方向等距的排列

        # 设置控件之间的间距
        hlayout.setSpacing(40)

        # 应用水平盒布局
        self.setLayout(hlayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = HBoxLayoutAlign()
    demo.show()
    sys.exit(app.exec_())
