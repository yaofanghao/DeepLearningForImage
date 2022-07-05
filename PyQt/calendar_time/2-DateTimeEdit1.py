"""
输入各种风格的日期和时间

QDateTimeEdit
"""
# 只想显示当前所设置的时间和日期

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DateTimeEdit1(QWidget):
    def __init__(self):
        super(DateTimeEdit1, self).__init__()
        self.initUI()

    # 编写初始化方法，规范代码，初始化写在一个方法里
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('设置不同风格的日期和时间')
        # 设置窗口尺寸
        self.resize(200,150)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建QDateTimeEdit控件
        # 第一个
        dateTimeEdit1 = QDateTimeEdit()
        # 第二个可以传入当前的时间和日期
        dateTimeEdit2 = QDateTimeEdit(QDateTime.currentDateTime())

        # 创建单独显示日期的控件
        # 第三个
        dateEdit = QDateTimeEdit(QDate.currentDate())

        # 创建单独显示时间的控件
        # 第四个
        timeEdit = QDateTimeEdit(QTime.currentTime())


        # 分别给这是四个控件设置显示日期或者时间的格式
        dateTimeEdit1.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        dateTimeEdit2.setDisplayFormat("yyyy/MM/dd HH-mm-ss")

        dateEdit.setDisplayFormat("yyyy.MM.dd")
        timeEdit.setDisplayFormat("HH:mm:ss")

        # 把控件添加到垂直布局里
        layout.addWidget(dateTimeEdit1)
        layout.addWidget(dateTimeEdit2)
        layout.addWidget(dateEdit)
        layout.addWidget(timeEdit)

        # 应用于垂直布局
        self.setLayout(layout)

# 防止其他脚本调用，直接运行此脚本，才会调用下面的代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = DateTimeEdit1()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，确保主循环安全退出
    sys.exit(app.exec_())

