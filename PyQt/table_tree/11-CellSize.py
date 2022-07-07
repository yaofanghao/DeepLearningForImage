"""
设置单元格尺寸
"""
import sys

from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)


class CellSize(QWidget):
    def __init__(self):
        super(CellSize, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QTableWidget 例子')
        self.resize(530,300)

        # 创建水平布局
        layout  = QHBoxLayout()

        # 创建表格控件
        tableWidget = QTableWidget()
        # 设置表格控件的行
        tableWidget.setRowCount(4)
        # 设置表格控件的列
        tableWidget.setColumnCount(3)

        # 创建字段
        newItem = QTableWidgetItem('活力')
        # 设置字体  字体大小
        newItem.setFont(QFont('Times',20,QFont.Black))
        # 设置字体颜色
        newItem.setForeground(QBrush(QColor(30,113,150)))
        # 设置单元格背景
        newItem.setBackground(QBrush(QColor(30,82,30)))

        # 把字段添加到表格里  第一行第一列
        tableWidget.setItem(0,0,newItem)

        # 创建字段
        newItem = QTableWidgetItem('18')
        # 设置字体  字体大小
        newItem.setFont(QFont('Times', 40, QFont.Black))

        #改变行的高度   第一个参数是行  第二个参数是设定值   第一行  高度80
        tableWidget.setRowHeight(0,120)
        # 把字段添加到表格里    第一行第二列
        tableWidget.setItem(0, 1, newItem)

        # 创建字段
        newItem = QTableWidgetItem('167')
        # 设置字体  字体大小
        newItem.setFont(QFont('Times', 60, QFont.Black))
        # 改变第三行的高度   第三行  高度80
        tableWidget.setRowHeight(2,20)
        # 改变列的高度   第一个参数是列  第二个参数是设定值   第三列  宽度120
        tableWidget.setColumnWidth(2,160)
        # 把字段添加到表格里   第一行第三列
        tableWidget.setItem(0, 2, newItem)

        # 把表格控件添加到布局里
        layout.addWidget(tableWidget)

        #应用于表格控件
        self.setLayout(layout)

# 直接执行此脚本，才会调用下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app =QApplication(sys.argv)
    # 创建对象
    main = CellSize()
    # 创建窗口
    main.show()
    # 创建主循环，调用exit方法，确保主循环安全退出
    sys.exit(app.exec_())
