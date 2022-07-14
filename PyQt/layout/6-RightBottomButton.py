"""
让按钮永远在窗口右下角

基本原理：
一分为二界面
上面任意布局
按钮放在水平布局里面
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RightBottomButton(QWidget):
    def __init__(self):
        super(RightBottomButton, self).__init__()
        self.setWindowTitle('让按钮永远在右下角')
        self.resize(400,300)

        # 添加两个按钮
        okButton = QPushButton("确定")
        cancelButton = QPushButton("取消")

        # 设置水平盒布局
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)


        # 设置垂直盒布局
        vbox = QVBoxLayout()
        btn1 = QPushButton('按钮1')
        btn2 = QPushButton('按钮2')
        btn3 = QPushButton('按钮3')
        btn4 =  QPushButton('按钮4')
        btn5 = QPushButton('按钮5')

        vbox.addStrut(0)
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)
        vbox.addWidget(btn5)

        # 把水平盒布局添加到垂直盒布局里
        vbox.addStrut(2)
        vbox.addLayout(hbox)


        # 应用于垂直盒布局
        self.setLayout(vbox)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = RightBottomButton()
    demo.show()
    sys.exit(app.exec_())
