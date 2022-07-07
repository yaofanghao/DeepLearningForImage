"""
在单元格中实现图文混排的效果
"""
# 让文本和图像 同时显示到一个单元格
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class CellImageText(QWidget):
    def __init__(self):
        super(CellImageText, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('在单元格实现图文混排的效果')
        self.resize(800,300)

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建全局表格控件
        self.tableWidget = QTableWidget()
        # 给表格控件设置行
        self.tableWidget.setRowCount(5)
        # 给表格控件设置列
        self.tableWidget.setColumnCount(4)

        # 给表格控件设置水平表头
        self.tableWidget.setHorizontalHeaderLabels(['姓名','性别','体重','显示图片'])

        # 创建字段
        # 添加QTableWidgetItem控件
        newItem = QTableWidgetItem('黎明')
        # 把字段控件放到表格控件里  第一行第一列
        self.tableWidget.setItem(0,0,newItem)


        newItem = QTableWidgetItem('男')
        # 把字段控件放到表格控件里  第一行第二列
        self.tableWidget.setItem(0, 1, newItem)



        newItem = QTableWidgetItem('18')
        # 把字段控件放到表格控件里  第一行第三列
        self.tableWidget.setItem(0, 2, newItem)


        # 第四列添加图片
        newItem = QTableWidgetItem(QIcon('../controls/images/001.png'),'背包')
        # 把newItem控件放到表格控件里 第一行第四列
        self.tableWidget.setItem(0,3,newItem)

        # 把表格控件添加到水平布局里面
        layout.addWidget(self.tableWidget)

        # 应用于水平布局
        self.setLayout(layout)

if __name__ == '__main__':
    app =QApplication(sys.argv)
    main = CellImageText()
    main.show()
    sys.exit(app.exec_())
