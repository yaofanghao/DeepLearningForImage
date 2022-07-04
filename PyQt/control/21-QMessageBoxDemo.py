"""
消息对话框 QMessageBox

主要用于显示版本和其他软件的信息

常用的有以下集中对话框
1.关于对话框
2.错误对话框
3.警告对话框
4.提问对话框
5.消息对话框

以上对话框主要有以下两种差异
1.显示的对话框图标可能不同
2.显示的按钮个数，文字是不一样的

"""

import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *

class QMessageBoxDemo(QWidget):
    def __init__(self):
        super(QMessageBoxDemo, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('QMessageBox演示')
        # 设置窗口尺寸
        self.resize(300,400)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建button1控件
        self.button1 = QPushButton()
        # 设置button1的文本内容
        self.button1.setText('显示关于对话框')

        # 创建button2控件
        self.button2 = QPushButton()
        # 设置button2的文本内容
        self.button2.setText('显示消息对话框')

        # 创建button3控件
        self.button3 = QPushButton()
        # 设置button3的文本内容
        self.button3.setText('显示警告对话框')

        # 创建button4控件
        self.button4 = QPushButton()
        # 设置button4的文本内容
        self.button4.setText('显示错误对话框')

        # 创建button5控件
        self.button5 = QPushButton()
        # 设置button5的文本内容
        self.button5.setText('显示提问对话框')

        # 信号与槽绑定  （本次演示，多个信号都绑定在一个槽上）
        self.button1.clicked.connect(self.showDialog)
        self.button2.clicked.connect(self.showDialog)
        self.button3.clicked.connect(self.showDialog)
        self.button4.clicked.connect(self.showDialog)
        self.button5.clicked.connect(self.showDialog)

        # 把控件添加到布局里
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)


        # 应用于垂直布局
        self.setLayout(layout)


    # 槽方法
    def showDialog(self):
        text = self.sender().text()
        if text == '显示关于对话框':
            QMessageBox.about(self,'关于','这是一个关于对话框')
        elif text == '显示消息对话框':
            # 两个选项，一个YES,一个No,还有一个默认的值，按回车之后会Yes
            reply = QMessageBox.information(self,'消息','这是一个消息对话框',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
            print(reply == QMessageBox.Yes)
        elif text == '显示警告对话框':
            QMessageBox.warning(self,'警告','这是一个警告对话框',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        elif text == '显示错误对话框':
            QMessageBox.critical(self, '错误', '这是一个错误对话框', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        elif text == '显示提问对话框':
            QMessageBox.question(self, '提问', '这是一个提问对话框', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QMessageBoxDemo()
    main.show()
    sys.exit(app.exec_())
