"""
用像素点绘制正弦曲线

drawPoint(x,y)
"""
# 绘制两个周期的正弦曲线  -2Π到2Π

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class DrawPoints(QWidget):
    def __init__(self):
        super(DrawPoints, self).__init__()
        # 设置窗口的大小
        self.resize(300,300)
        # 设置窗口标题
        self.setWindowTitle('在窗口上用像素点绘制2个周期的正弦曲线')

    def paintEvent(self,event):
        painter =QPainter()
        painter.begin(self)
        # 设置笔的颜色 固定 方法二
        painter.setPen(Qt.blue)
        # 获得窗口尺寸
        size = self.size()
        # 对水平轴进行循环，循环一千次
        for i in range(1000):
            x = 100 * (-1 + 2.0 * i/1000) + size.width()/2.0
            # pi 指的是Π
            y = -50 * math.sin((x - size.width()/2.0)* math.pi/50) + size.height()/2.0
            painter.drawPoint(x,y)


        painter.end()

# 防止别的脚本调用，只有自己单独运行时，才会执行下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = DrawPoints()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，确保主循环安全结束
    sys.exit(app.exec_())
