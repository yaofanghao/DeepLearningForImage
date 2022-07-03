# 按钮控件(QPushButton)
# 按钮有多个控件，它的父类QAbstractButton
# 子类有： QPushButton   AToolButton(工具条按钮) QRadioButton(单选按钮)  QCheckBox(复选按钮)

import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *


# 创建一个类,基于QDialog    QDialog是对话窗口的基类。没有菜单栏、工具栏、状态栏
class QPushButtonDemo(QDialog):
    def __init__(self):
        super(QPushButtonDemo,self).__init__()
        self.initUI()

    # 编写初始化方法，规范代码，初始化写在一个方法里
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('QPushButton Demo')

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建四个button
        self.button1 = QPushButton('第1个按钮')
        # 通过setText获得文本
        self.button1.setText('First Button1')
        # 设置按钮按下自动弹起
        # # 按钮可复选的，可核对的
        self.button1.setCheckable(True)
        # 设置开关
        self.button1.toggle()
        # 上面两行代码，此时setCheckable为True时，调用toggle方法，按钮为选中状态，再调一次toggle方法时，处于未选中状态
        # 把槽绑定到单击按钮信号上
        # 通过两种方式将信息和槽相连
        # 信号和槽相连 方式一
        self.button1.clicked.connect(lambda :self.whichButton(self.button1))
        # 两个信号绑定到一个槽上   信号和槽是多对多的关系
        # 信号和槽相连 方式二
        self.button1.clicked.connect(self.buttonState)


        # 创建button2控件  在文本前显示图像
        self.button2 = QPushButton('图像按钮')
        # 给button2设置图形
        self.button2.setIcon(QIcon(QPixmap('./images/001.jpg')))
        # 把button2与槽连接
        self.button2.clicked.connect(lambda:self.whichButton(self.button2))


        # 创建button3控件，让按钮不可用
        self.button3 = QPushButton('不可用的按钮')
        # 设置按钮不可用
        self.button3.setEnabled(False)


       # 创建button4控件，为默认按钮(点回车可以执行的按钮)，并给它加热键  按Alt + M 就可以直接调用这个button
        # 默认按钮一个窗口只能有一个
        self.button4 = QPushButton('&MyButton')
        # 设置button4按钮为默认按钮
        self.button4.setDefault(True)
        # 把button4与槽连接
        self.button4.clicked.connect(lambda :self.whichButton(self.button4))

        # 把控件添加到布局里
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)

        # 应用于垂直布局
        self.setLayout(layout)
        # 设置窗口尺寸
        self.resize(400,300)

    # 编写槽函数
    # 多个按钮多个信号，同时使用一个槽，需要区分到底按了哪一个按钮
    # 目前有两种方法
    #第一种，用sender()方法
    # def whichButton(self):
        # self.sender()
    # 第二种，传参数，比如
    def whichButton(self,btn):
        print('被单击的按钮是<' + btn.text() + '>')

    # 编写第二个槽
    def buttonState(self):
        # 判断是否被选中
        if self.button1.isChecked():
            print('按钮1已经被选中')
        else:
            print('按钮1未被选中')


 # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)

    # 设置图标
    # app.setWindowIcon(QIcon('images/001.jpg'))

    # 创建对象
    main = QPushButtonDemo()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
