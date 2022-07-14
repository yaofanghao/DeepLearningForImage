"""
设置伸缩量(addStretch)

有多种方式，
HBoxLayoutAlign.py中
hlayout.addWidget(QPushButton('按钮1'),1,Qt.AlignLeft | Qt.AlignTop) 中的第二个参数 1 就是伸缩量
"""



import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Stretch(QWidget):
    def __init__(self):
        super(Stretch, self).__init__()
        self.setWindowTitle("设置伸缩量")
        self.resize(800,400)

        # 添加三个按钮
        btn1 = QPushButton(self)
        btn2 = QPushButton(self)
        btn3 = QPushButton(self)
        btn4 = QPushButton(self)
        btn5 = QPushButton(self)
        # 分别设置文本
        btn1.setText('按钮1')
        btn2.setText('按钮2')
        btn3.setText('按钮3')
        btn4.setText('按钮4')
        btn5.setText('按钮5')

        # 放置水平布局
        layout = QHBoxLayout()


        # 把三个按钮添加到布局里
        layout.addStretch(0)
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)
        layout.addWidget(btn5)


        btnOK = QPushButton(self)
        btnOK.setText("确定")

        layout.addStretch(1)
        layout.addWidget(btnOK)

        btnCancel = QPushButton(self)
        btnCancel.setText("取消")

        layout.addStretch(2)
        layout.addWidget(btnCancel)


        # 应用于水平布局
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Stretch()
    demo.show()
    sys.exit(app.exec_())
