"""
使用线程类(QThread)编写计数器

基本原理
QThread派生一个子类
在这个子类里面定义一个run方法
def run(self):
    while True:
    # 每循环一次，休眠一秒钟
        self.sleep(1)
        # 当前循环等于5，直接退出
        if sec == 5:
            break;

QLCDNumber控件


WorkThread(QThread)
用到自定义信号
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# 定义一个变量
sec = 0
class WorkThread(QThread):
    timer = pyqtSignal()   # 每隔1秒发送一次信号
    end = pyqtSignal()     # 计数完成后发送一次信号
    def run(self):
        while True:
            self.sleep(1)  # 休眠1秒
            if sec == 5:
                self.end.emit() # 发送end信号
                break
            self.timer.emit()  # 发送timer信号


class Counter(QWidget):
    def __init__(self,parent=None):
        super(Counter, self).__init__(parent)

        self.setWindowTitle("使用线程类(QThread)编写计数器")
        self.resize(300,200)

        # 创建垂直布局
        layout = QVBoxLayout()
        self.lcdNumber = QLCDNumber()
        layout.addWidget(self.lcdNumber)

        button = QPushButton('开始计数')
        layout.addWidget(button)

        # 创建工作线程对象
        self.workThread = WorkThread()

        # 绑定 信号 槽
        self.workThread.timer.connect(self.countTime)
        self.workThread.end.connect(self.end)
        # 槽和按钮的单击事件
        button.clicked.connect(self.work)

        # 应用于垂直布局
        self.setLayout(layout)

    # 槽方法
    def countTime(self):
        # global 声明全局变量
        global sec
        sec += 1
        self.lcdNumber.display(sec)

    def end(self):
        QMessageBox.information(self,'消息','计数结束',QMessageBox.Ok)

    def work(self):
        self.workThread.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo =Counter()
    demo.show()
    sys.exit(app.exec_())

