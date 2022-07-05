"""
绘制各种图形
弧 圆形 矩形(正方形) 多边形 绘制图像
"""

import sys,math

from PyQt5.QtWidgets import *
from  PyQt5.QtGui import *
from  PyQt5.QtCore import *

class DrawAll(QWidget):
    def __init__(self):
        super(DrawAll, self).__init__()
        self.resize(400,600)
        self.setWindowTitle('绘制各种图形')

    # 定义事件
    def paintEvent(self, event):
        # 创建一个Qpainter对象
        qp = QPainter()
        # 绘制开始
        qp.begin(self)

        # 设置笔的颜色
        qp.setPen(Qt.blue)

        # 绘制弧
        #  确定一个区域
        rect = QRect(0,10,100,100)
        # alen:一个alen等于1/16度   所以表示45度，用45*16表示
        #  画50度，用50*16表示  参数  起  终
        qp.drawArc(rect,0,50*16)

        # 通过弧绘制圆
        #  更改笔的颜色
        qp.setPen(Qt.red)
        # 位置 从0 到360°
        qp.drawArc(120,10,100,100,0, 360* 16)

        # 绘制带弦的弧
        # 位置 从12°到130°
        qp.drawChord(10,120,100,100,12,130*16)

        # 绘制扇形
        #  位置  从12°到130°
        qp.drawPie(10,240,100,100,12,130*16)

        # 椭圆
        #  不需要指定开始角度和结束角度     宽和高不一样。 如果一样就成圆了
        qp.drawEllipse(120,120,150,100)
        # 通过椭圆绘制圆   距窗口的宽  距窗口的高   宽  高
        qp.drawEllipse(180, 300, 150, 150)


        # 绘制五边形
        #   需要指定五个点
        point1 = QPoint(140,380)
        point2 = QPoint(270,420)
        point3 = QPoint(290,512)
        point4 = QPoint(290,588)
        point5 = QPoint(200,533)

        #   创建一个多边形的对象
        polygon = QPolygon([point1,point2,point3,point4,point5])
        #  开始绘制五边形
        qp.drawPolygon(polygon)

        # 绘制图像
        #   装载图像
        image = QImage('./images/001.jpg')
        #   指定绘制图像的区域   把图片缩小到原来的三分之一
        #    距离窗口的宽度  距离窗口的高度   宽缩小三分之一  高缩小三分之一
        rect = QRect(10,400,image.width()/3,image.height()/3)
        image.save('../controls/images/5.png')
        # 开始绘制图像
        qp.drawImage(rect,image)

        # 绘制结束
        qp.end()

# 防止其他脚本调用，只有当这个脚本自己运行时，才会调用下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = DrawAll()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit函数，确保主循环安全结束
    sys.exit(app.exec_())

