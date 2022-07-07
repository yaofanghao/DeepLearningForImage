"""
合并单元格
setSpan(row,col,要合并的行数,要合并的列数)

"""
import sys
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)


class Span(QWidget):
    def __init__(self):
        super(Span, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('合并单元格')
        self.resize(430,230)

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建表格控件
        tableWidget = QTableWidget()
        # 设置表格的行数
        tableWidget.setRowCount(4)
        # 设置表格的列数
        tableWidget.setColumnCount(3)

        # 把表格控件添加到布局里
        layout.addWidget(tableWidget)

        # 创建水平表头
        tableWidget.setHorizontalHeaderLabels(['姓名','年龄','身高'])

        # 创建字段
        newItem = QTableWidgetItem('大卫')
        # newItem添加到表格里 第一行第一列
        tableWidget.setItem(0,0,newItem)
        # 合并第一行第一列  ，合并3行，合并一列
        tableWidget.setSpan(0,0,3,1)

        # 创建字段
        newItem = QTableWidgetItem('18')
        # newItem添加到表格里  第一行第二列
        tableWidget.setItem(0, 1, newItem)
        # 合并第一行第二列   合并两行，合并一列
        tableWidget.setSpan(0,1,2,1)

        # 创建字段
        newItem = QTableWidgetItem('180')
        # newItem添加到表格里   第一行第三列
        tableWidget.setItem(0, 2, newItem)
        # 合并第一行第三列  合并4行 合并一列
        tableWidget.setSpan(0,2,4,1)

        # 创建字段
        newItem = QTableWidgetItem('测试')
        # newItem添加到表格里   第四行第一列
        tableWidget.setItem(3, 0, newItem)
        # 合并第四行第一  合并一行 合并两列
        tableWidget.setSpan(3, 0, 1, 2)

        # 应用于水平布局
        self.setLayout(layout)

# 直接调用该脚本，执行下面代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = Span()
    # 创建窗口
    main.show()
    # 进入主循环，调用exit方法，确保主循环安全退出
    sys.exit(app.exec_())
