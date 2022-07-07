"""
设置单元格字体和颜色
"""

import sys
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)
from PyQt5.QtGui import QBrush,QColor,QFont

class CellFontAndColor(QWidget):
    def __init__(self):
        super(CellFontAndColor, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle("设置单元格字体和颜色")
        # 设置窗口的尺寸
        self.resize(600,300)

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建QTableWidget控件
        tableWidget = QTableWidget()
        # 设置tableWidget的行
        tableWidget.setRowCount(4)
        # 设置tableWidget的列
        tableWidget.setColumnCount(3)

        # 把控件放置在布局里
        layout.addWidget(tableWidget)
        # 设水平表头
        tableWidget.setHorizontalHeaderLabels(['姓名','性别','体重(kg)'])


        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('水手')
        # 字号 字体
        newItem.setFont(QFont('Times',14,QFont.Black))
        # 设置字颜色
        newItem.setForeground(QBrush(QColor(255,0,0)))

        # 添加到第一行第一列
        tableWidget.setItem(0,0,newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('大海')
        # 设置字的颜色
        newItem.setForeground(QBrush(QColor(255,200,0)))
        # 设置背景色
        newItem.setBackground(QBrush(QColor(0,0,220)))

        # 添加到第一行第二列
        tableWidget.setItem(0,1,newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('你好')
        # 设置字的颜色
        newItem.setFont(QFont('Times', 25, QFont.Black))
        newItem.setForeground(QBrush(QColor(125, 50, 0)))
        # 设置背景色
        newItem.setBackground(QBrush(QColor(0, 0, 20)))

        # 添加到第一行第二列
        tableWidget.setItem(0, 2, newItem)

        # 应用于水平布局
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = CellFontAndColor()
    example.show()
    sys.exit(app.exec_())
