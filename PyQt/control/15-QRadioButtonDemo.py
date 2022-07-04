"""
单选按钮控件(QRadioButton)
"""
import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *


class RadioButtonDemo(QWidget):
    def __init__(self):
        super(RadioButtonDemo,self).__init__()
        self.initUI()

    def initUI(self):

        # 设置窗口标题
        self.setWindowTitle('QRadioButton')
        # 把是所有的单选按钮都放在一个容器里，才能实现单选


        # 创建水平布局
        layout = QHBoxLayout()

        # 创建button1控件
        self.button1 = QRadioButton('单选按钮1')
        # 设button1默认为选中状态
        self.button1.setChecked(True)


        # 创建button2控件
        self.button2 = QRadioButton('单选按钮2')


        # 连接信息槽
        # toggle是状态切换的信号
        self.button1.toggled.connect(self.buttonState)
        self.button2.toggled.connect(self.buttonState)


        # 把控件添加到水平布局里
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)


        # 应用于水平布局
        self.setLayout(layout)


    # 编写槽
    # def buttonState(self):
    #     # 控件获取数据
    #     radioButton = self.sender()
    #     # 判断获取的数据的文本是否是‘单选按钮1’
    #     if radioButton.text() == '单选按钮1':
    #         # 判断获取的数据的文本是‘单选按钮1’的是否被选中
    #         if radioButton.isChecked() == True:
    #             # 如果被选中
    #             print('<' + radioButton.text() + '>被选中' )
    #         else:
    #             print('<' + radioButton.text() + '>被取消选中状态')
    #     # 判断获取的数据的文本是否是‘单选按钮2’
    #     if radioButton.text() == '单选按钮2':
    #         # 判断获取的数据的文本是‘单选按钮2’的是否被选中
    #         if radioButton.isChecked() == True:
    #             # 如果被选中
    #             print('<' + radioButton.text() + '>被选中')
    #         else:
    #             print('<' + radioButton.text() + '>被取消选中状态')
    def buttonState(self):
        # 控件获取数据
        radioButton = self.sender()
        if radioButton.isChecked() == True:
            # 如果被选中
            print('<' + radioButton.text() + '>被选中')
        else:
            print('<' + radioButton.text() + '>被取消选中状态')

# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = RadioButtonDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())

