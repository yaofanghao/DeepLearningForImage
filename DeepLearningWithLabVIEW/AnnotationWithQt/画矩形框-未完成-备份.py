# 未完成内容：
# 图片应该可以缩放，而不是自动resize
# 将标注的矩形框编号，并存储对应的位置信息
# https://blog.csdn.net/weixin_38243861/article/details/91972698

# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtWidgets, QtGui

class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        self.setWindowTitle("绘图例子")
        # 实例化QPixmap类
        self.pix = QPixmap()
        # 起点，终点
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        # 初始化
        self.initUi()

    def initUi(self):
        self.resize(1000, 800)  # 窗口大小设置为600*500，这样可以鼠标拖动缩放
        # self.setFixedSize(600, 500)  # 固定窗口大小，不可缩放

        # 画布大小为400*400，背景为白色
        self.pix = QPixmap(800, 800)
        self.pix.fill(Qt.white)

        # 偏移量，保证鼠标的位置和画的线点是重合的
        self.offset = QPoint(self.width() - self.pix.width(), self.height() - self.pix.height())

        btn_clear = QPushButton(self)
        btn_clear.setText("清空")
        btn_clear.resize(80, 30)
        btn_clear.move(10, 30)
        btn_clear.clicked.connect(self.clear)

        btn_save = QPushButton(self)
        btn_save.setText("保存")
        btn_save.resize(80, 30)
        btn_save.move(10, 80)
        btn_save.clicked.connect(self.save)

        btn_open = QPushButton(self)
        btn_open.setText("打开")
        btn_open.resize(80, 30)
        btn_open.move(10, 130)
        btn_open.clicked.connect(self.open)

    def clear(self):
        self.pix.fill(Qt.white)
        self.update()

    def save(self):
        self.pix.save("draw.jpg")

    def open(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QPixmap(imgName).scaled(self.pix.width(), self.pix.height())
        # jpg = QPixmap(imgName).scaled(imgName.width(), imgName.height())
        # self.label.setPixmap(jpg)
        self.pix = jpg

    def paintEvent(self, event):
        """
        重载绘制事件。
        将self.pix中的内容复制到缓存中，在缓存上绘图。
        """
        x = self.lastPoint.x()
        y = self.lastPoint.y()
        w = self.endPoint.x() - x
        h = self.endPoint.y() - y

        self.temp = self.pix.copy()  # 如果直接赋值，两者的内存是相同的，因此这里需要调用copy。
        pp = QPainter(self.temp)
        pp.drawRect(x, y, w, h)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.temp)

    def mousePressEvent(self, event):
        """
        按下鼠标左键后，将当前位置存储到起点中。
        """
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
        print("position is ")
        print(event.pos())

    def mouseMoveEvent(self, event):
        """
        鼠标左键被按下且在滑动中，调用绘图函数，更新画布内容。
        """
        if event.buttons() and Qt.LeftButton:  # 这里的写法非常重要
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """
        松开鼠标左键后，将当前位置存储到终点中；绘制图案，并将缓存中的内容更新到self.pix中。
        """
        self.endPoint = event.pos()
        self.update()
        self.pix = self.temp.copy()
        print(event.pos())
        print("-------------")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Winform()
    form.show()
    sys.exit(app.exec_())