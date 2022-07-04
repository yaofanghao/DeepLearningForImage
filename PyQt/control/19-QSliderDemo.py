"""
滑块控件
通过滑块左右或者上下拉动来控制数字变化
"""
# 如何通过滑块标签来设置字体的大小

import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *


class QSliderDemo(QWidget):
    def __init__(self):
        super(QSliderDemo, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('滑块控件演示')
        # 设置窗口尺寸
        self.resize(300,300)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建label控件
        self.label = QLabel('你好，PyQt5')
        # 让label控件居中显示
        self.label.setAlignment(Qt.AlignCenter)




        # 创建滑块控件，有两种：水平和垂直
        # 创建水平的滑块控件slider
        self.slider = QSlider(Qt.Horizontal)
        # 创建垂直的滑块控件slider1
        self.slider1 =   QSlider(Qt.Vertical)

        # 设置最小值12
        self.slider.setMinimum(12)
        self.slider1.setMinimum(12)
        # 设置最大值
        self.slider.setMaximum(58)
        self.slider1.setMaximum(58)
        # 步长
        self.slider.setSingleStep(3)
        self.slider1.setSingleStep(3)
        # 设置当前值
        self.slider.setValue(18)
        self.slider1.setValue(12)
        # 设置刻度的位置，刻度在下方
        self.slider.setTickPosition(QSlider.TicksBelow)
        # 设置刻度的位置，刻度在左方
        self.slider1.setTickPosition(QSlider.TicksLeft)
        # 设置刻度的间隔
        self.slider.setTickInterval(6)
        self.slider1.setTickInterval(3)

        # 把控件添加到垂直布局里
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.slider1)

        #信号槽的绑定
        self.slider.valueChanged.connect(self.valueChange)
        self.slider1.valueChanged.connect(self.valueChange)

        # 应用于垂直布局
        self.setLayout(layout)

    # 槽方法
    def valueChange(self):
        print('slider当前值：%s' % self.slider.value())
        print('slider1当前值：%s' % self.slider1.value())
        # 获得值
        size = self.slider.value()
        size = self.slider1.value()
        # 设置字体字号，让字号通过值发生变化
        self.label.setFont(QFont('Arial',size))


# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QSliderDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())
