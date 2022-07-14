"""
选项卡控件：QTabWidget

目的：在屏幕上显示更多的控件  在页面中显示多页面
"""


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TabWidgetDemo(QTabWidget):
    def __init__(self,parent=None):
        super(TabWidgetDemo, self).__init__(parent)

        self.setWindowTitle('选项卡控件:QTabWidget')
        self.resize(600,400)

        # QTableView的最终父类是QWidget  将整个窗口作为一个tab

        # 创建多个窗口  每个窗口可以放置多个控件
        # 创建用于显示控件的窗口
        # 创建窗口tab1
        self.tab1 = QWidget()
        # 创建窗口tab2
        self.tab2 = QWidget()
        # 创建窗口tab3
        self.tab3 = QWidget()

        # 把每个窗口和选项卡绑定
        self.addTab(self.tab1,'选项卡1')
        self.addTab(self.tab2,'选项卡2')
        self.addTab(self.tab3,'选项卡3')

        # 调用
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    # 为每个选项卡单独编写一个方法
    def tab1UI(self):
        # 创建表单布局
        layout = QFormLayout()
        layout.addRow('姓名',QLineEdit())
        layout.addRow('地址',QLineEdit())
        self.setTabText(0,'联系方式')
         # 装载
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton('男'))
        sex.addWidget(QRadioButton('女'))
        layout.addRow(QLabel('性别'),sex)
        layout.addRow('生日',QLineEdit())
        self.setTabText(1,'个人详细信息')
        self.tab2.setLayout(layout)

    def tab3UI(self):
        # 放置水平布局
        layout = QHBoxLayout()
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))
        self.setTabText(2,'教育程序')
        self.tab3.setLayout(layout)


if __name__ == '__main__':
    app =QApplication(sys.argv)
    demo = TabWidgetDemo()
    demo.show()
    sys.exit(app.exec_())

