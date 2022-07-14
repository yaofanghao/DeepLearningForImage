"""
动态显示当前时间

QTimer  定时器  每隔一定时间会调用一次
QThread

多线程用于同时完成多个任务    在单CPU上是按顺序完成的(时间片切换)，从宏观上来看，还是同时完成的
                         在多CPU上，是可以真正的同时完成
"""

import sys
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout,QLabel
from PyQt5.QtCore import QTimer,QDateTime


class ShowTime(QWidget):
    def __init__(self,parent=None):
        super(ShowTime, self).__init__(parent)
        # 设置窗口标题
        self.setWindowTitle("动态显示当前时间")

        # 创建QLabel控件
        self.label = QLabel('显示当前时间')
        # 创建button按扭
        self.startBtn = QPushButton('开始')
        # 创建button按钮
        self.endBtn = QPushButton('结束')


        # 通过栅格布局，安排这三个控件的位置
        layout = QGridLayout()

        # 设置定时器对象
        self.timer = QTimer()
        # 时间的 信号 槽
        self.timer.timeout.connect(self.showTime)

        # 把这三个控件放到栅格布局里面
        # 在第一行第一列   占用一行  占用两列
        layout.addWidget(self.label,0,0,1,2)
        # 在第二行第一列
        layout.addWidget(self.startBtn,1,0)
        # 在第二行第二列
        layout.addWidget(self.endBtn,1,1)

        # 开始控件的信号 槽
        self.startBtn.clicked.connect(self.startTimer)
        # 结束控件的信号 槽
        self.endBtn.clicked.connect(self.endTimer)

        # 应用于栅格布局
        self.setLayout(layout)

    # 槽方法
    # 显示时间
    def showTime(self):
        # 获取当前的时间
        time = QDateTime.currentDateTime()
        # 设置时间显示
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.label.setText(timeDisplay)

    def startTimer(self):
        # 开始时间 1s
        self.timer.start(1000)
        # 开始之后开始按钮关闭
        self.startBtn.setEnabled(False)
        # 开始之后关闭按钮开始
        self.endBtn.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        # 开始之后开始按钮开始
        self.startBtn.setEnabled(True)
        # 开始之后关闭按钮关闭
        self.endBtn.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ShowTime()
    demo.show()
    sys.exit(app.exec_())
