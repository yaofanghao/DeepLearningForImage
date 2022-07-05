"""
用画刷填充图形区域
"""

import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class FillRect(QWidget):
    def __init__(self):
        super(FillRect, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('用画刷填充区域')
        # 设置窗口尺寸
        self.resize(600,600)

    # 定义事件
    def paintEvent(self, e):
        # 创建QPainter对象
        qp = QPainter()
        # 绘制开始
        qp.begin(self)
        # 创建画刷对象  默认实心
        brush = QBrush(Qt.SolidPattern)
        # 设置画刷
        qp.setBrush(brush)

        # 绘制矩形，填充区域
        #   距窗口的宽   距窗口的高    绘制矩形的宽   绘制矩形的高
        qp.drawRect(30,15,150,60)

        # 创建画刷
        brush1 = QBrush(Qt.Dense1Pattern)
        # 设置画刷
        qp.setBrush(brush1)
        # 绘制矩形，填充区域
        #   距窗口的宽   距窗口的高    绘制矩形的宽   绘制矩形的高
        qp.drawRect(30,100,150,60)

        # 创建画刷
        brush2 = QBrush(Qt.Dense2Pattern)
        # 设置画刷
        qp.setBrush(brush2)
        # 绘制矩形，填充区域
        #   距窗口的宽   距窗口的高    绘制矩形的宽   绘制矩形的高
        qp.drawRect(30, 180, 150, 60)

        # 创建画刷
        brush3 = QBrush(Qt.Dense3Pattern)
        # 设置画刷
        qp.setBrush(brush3)
        # 绘制矩形，填充区域
        #   距窗口的宽   距窗口的高    绘制矩形的宽   绘制矩形的高
        qp.drawRect(30, 260, 150, 60)

        # 创建画刷
        brush4 = QBrush(Qt.HorPattern)
        # 设置画刷
        qp.setBrush(brush4)
        # 绘制矩形，填充区域
        #   距窗口的宽   距窗口的高    绘制矩形的宽   绘制矩形的高
        qp.drawRect(30, 340, 150, 60)

        # 绘制结束
        qp.end()

# 防止其他脚本调用，单独调用此脚本，才会执行下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = FillRect()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，确保主循环安全结束
    sys.exit(app.exec_())
