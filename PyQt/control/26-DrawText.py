"""
绘制API:绘制文本

绘制API主要有三种类型
1.文本
2.各种图形(直线、点、椭圆、弧、扇形、多边形等)
3.图像

绘制元素的类QPainter

大致过程
painter = QPainter()
painter.begin()
painter.drawText(...)
painter.end()

必须在paintEvent事件方法中绘制各种元素
这个事件自动调用，在创建窗口时，以及窗口尺寸发生变化时，会重新绘制，很快

本质上， 窗口尺寸改变时，窗口上的所有元素都会重新绘制

"""
import sys
from PyQt5.QtWidgets import  QApplication,QWidget
from PyQt5.QtGui import QPainter,QColor,QFont
from PyQt5.QtCore import Qt

class DrawText(QWidget):
    def __init__(self):
        super(DrawText, self).__init__()
        # 创建窗口标题
        self.setWindowTitle('在窗口上绘制文本')
        # 设置窗口尺寸
        self.resize(600,200)
        # 设置文本
        self.text = "PyQt5从入门到精通"

    # 定义事件方法
    # 参数两个，一个它自己，一个是event
    def paintEvent(self, event):
        # 创建QPainter对象
        painter = QPainter()
        painter.begin(self)
        print('aaaa')
        # 设置笔的颜色
        painter.setPen(QColor(123,21,3))
        # 设置字体和字号
        painter.setFont(QFont('SimSun',25))
        # 指定区域，设置对齐方式 居中
        painter.drawText(event.rect(),Qt.AlignCenter,self.text)
        painter.end()

# 防止别的脚本调用，只有自己单独运行时，才会执行下面的代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = DrawText()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法
    sys.exit(app.exec_())
