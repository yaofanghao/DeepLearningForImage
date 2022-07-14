"""
堆栈窗口控件(QStackedWidget)

通过切换来显示不同页的控件
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class StackedExample(QWidget):
    def __init__(self):
        super(StackedExample, self).__init__()
        # 从屏幕宽500，高200的位置显示出一个宽300，高200的窗口
        self.setGeometry(500,200,300,200)
        self.setWindowTitle("堆栈窗口控件(QStackedWidget)")


        # 放置列表控件
        self.list = QListWidget()
        # 在列表的第一列添加 "联系方式"
        self.list.insertItem(0,"联系方式")
        # 在列表的第二列添加  "个人信息"
        self.list.insertItem(1,"个人信息")
        # 在列表的第三列添加  "教育程序"
        self.list.insertItem(2,"教育程度")


        # 创建三个页面
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()

        # 调用
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        # 创建堆栈窗口对象
        self.stack = QStackedWidget()
        # 把这三个窗口添加到堆栈窗口里面
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)

        # 创建水平布局 左侧显示列表  右侧显示堆栈页面
        hbox = QHBoxLayout()
        hbox.addWidget(self.list)
        hbox.addWidget(self.stack)
        # 应用于水平布局
        self.setLayout(hbox)

        # 为列表添加事件  当前行变化 信号 槽绑定
        self.list.currentRowChanged.connect(self.display)

    # 编写三个槽方法
    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow('姓名',QLineEdit())
        layout.addRow('地址',QLineEdit())
        self.stack1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton('男'))
        sex.addWidget(QRadioButton('女'))
        layout.addRow(QLabel('性别'),sex)
        layout.addRow('生日',QLineEdit())
        self.stack2.setLayout(layout)

    def tab3UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('科目'))
        layout.addWidget(QCheckBox('物理'))
        layout.addWidget(QCheckBox('高数'))

        self.stack3.setLayout(layout)


    def display(self,index):
        # index 为当前项的变化
        # 根据索引切换栈里面的页面
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QStackedWidget()
    main.show()
    sys.exit(app.exec_())
