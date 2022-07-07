"""
改变单元格中的图片尺寸

setIconSize(QSize(width,height))
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CellImageSize(QWidget):
    def __init__(self):
        super(CellImageSize, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('改变单元格中图片的尺寸')
        self.resize(800,600)

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建表格控件
        tablewidget = QTableWidget()
        # 设置表格行
        tablewidget.setRowCount(5)
        # 设置表格列
        tablewidget.setColumnCount(3)
        # 设置表格内图像的尺寸
        tablewidget.setIconSize(QSize(200,80))

        # 设置水平表头
        tablewidget.setHorizontalHeaderLabels(['图片1','图片2','图片3'])

        # 让列的宽度和图片的宽度相同
        for i in range(3):
            tablewidget.setColumnWidth(i,200)

        # 让行的高度和图片的高度相同
        for i in range(5):
            tablewidget.setRowHeight(i,80)

        # 添加图片
        # 如果有15张图片
        for k in range(15):
            i = k / 3  # 行
            j = k % 3  # 列
            item = QTableWidgetItem()
            item.setIcon(QIcon('./images/00%s.jpg'% k))
            tablewidget.setItem(i,j,item)

        # 把表格控件添加到水平布局里
        layout.addWidget(tablewidget)

        # 应用于水平布局
        self.setLayout(layout)

if __name__ == '__main__':
    app =QApplication(sys.argv)
    main = CellImageSize()
    main.show()
    sys.exit(app.exec_())
