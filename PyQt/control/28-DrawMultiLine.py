"""
绘制不同类型的直线

"""
import sys, math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class DrawMultiLine(QWidget):
    def __init__(self):
        super(DrawMultiLine, self).__init__()
        self.resize(300, 300)
        self.setWindowTitle('设置Pen的样式')

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        # 创建画笔   设置颜色，粗细  类型(实线，虚线)
        pen = QPen(Qt.red, 3, Qt.SolidLine)

        # 设置对象
        painter.setPen(pen)
        # 绘图
        painter.drawLine(20, 40, 250, 40)

        # 设置虚线
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(20, 80, 250, 80)

        # 设置点划线
        pen.setStyle(Qt.DashDotDotLine)
        painter.setPen(pen)
        painter.drawLine(20, 120, 250, 120)

        # 设置虚线
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawLine(20, 160, 250, 160)

        # 设置自定义
        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([1, 2])
        painter.setPen(pen)
        painter.drawLine(20, 200, 20, 200)

        size = self.size()

        # 绘制结束
        painter.end()


# 防止其他脚本调用，只有运行该脚本时，才会执行下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = DrawMultiLine()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，保证主循环安全结束
    sys.exit(app.exec_())
