"""
滚动条控件(QScrollBar)

本身不是容器，但是可以起到容器的作用
QScrollBar的作用：
1.通过滚动条值的变化控制其他控件状态的变化
2.通过滚动条值的变化控制控件位置的变化

"""
# 用三个滚动条控件控制文本的颜色变化
# 用一个滚动条控件控制QLableEdit控件的上下移动
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ScrollBar(QWidget):
    def __init__(self):
        super(ScrollBar, self).__init__()
        self.initUI()

    def initUI(self):
        # 创建水平布局
        hbox = QHBoxLayout()
        # 创建label,用来控制文本的颜色以及移动
        self.label = QLabel('拖动滚动条去改变文字颜色')

        # 把label添加到水平布局里
        hbox.addWidget(self.label)

        # 创建三个滚动条控件
        # 创建第一个滚动条
        self.scrollbar1 = QScrollBar()
        # 设置第一个滚动条的最大值    最小为0
        self.scrollbar1.setMaximum(255)
        # 设置信号 滚动条移动  这三个滚动条都使用同一个槽
        self.scrollbar1.sliderMoved.connect(self.sliderMoved)

        # 创建第二个滚动条
        self.scrollbar2 = QScrollBar()
        # 设置第一个滚动条的最大值    最小为0
        self.scrollbar2.setMaximum(255)
        # 设置信号 滚动条移动  这三个滚动条都使用同一个槽
        self.scrollbar2.sliderMoved.connect(self.sliderMoved)

        # 创建第三个滚动条
        self.scrollbar3 = QScrollBar()
        # 设置第一个滚动条的最大值    最小为0
        self.scrollbar3.setMaximum(255)
        # 设置信号 滚动条移动  这三个滚动条都使用同一个槽
        self.scrollbar3.sliderMoved.connect(self.sliderMoved)

        # 创建第四个滚动条   用来移动位置
        self.scrollbar4 = QScrollBar()
        # 设置第一个滚动条的最大值    最小为0
        self.scrollbar4.setMaximum(255)
        # 设置信号 滚动条移动  这三个滚动条都使用同一个槽
        self.scrollbar4.sliderMoved.connect(self.sliderMoved1)

        # 把这三个滚动条都添加到水平布局里
        hbox.addWidget(self.scrollbar1)
        hbox.addWidget(self.scrollbar2)
        hbox.addWidget(self.scrollbar3)
        hbox.addWidget(self.scrollbar4)

        # 设置当前窗口的位置坐标
        # 距离屏幕宽300，高300的位置，创建一个宽300高200的窗口
        self.setGeometry(300,300,300,200)




        # 应用于水平布局
        self.setLayout(hbox)


        # 保留当前的坐标   用来移动位置
        self.y = self.label.pos().y()

    # 槽方法
    def sliderMoved(self):
        # 打印当前设的值
        print(self.scrollbar1.value(),self.scrollbar2.value(),self.scrollbar3.value())
        # 设置调试板
        palette = QPalette()
        # 设置颜色
        c = QColor(self.scrollbar1.value(),self.scrollbar2.value(),self.scrollbar3.value(),255)
        palette.setColor(QPalette.Foreground,c)
        self.label.setPalette(palette)

    # 用button4演示移动
    def sliderMoved1(self):
        # x轴坐标不变，用来垂直移动
        self.label.move(self.label.x(),self.y + self.scrollbar4.value())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo= ScrollBar()
    demo.show()
    sys.exit(app.exec_())
