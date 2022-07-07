"""
扩展的表格控件(QTableWidget)
是在QTableView上面进行扩展

每一个Cell(单元格)是一个QTableWidgetItem
"""
import sys
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem, QAbstractItemView)


class TableWidgetDemo(QWidget):
    def __init__(self):
        super(TableWidgetDemo, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle("QTableWidget演示")
        # 设置窗口尺寸
        self.resize(430,230)

        # 创建一个水平布局
        layout = QHBoxLayout()

        # 创建一个QTableWidget控件
        tableWidget = QTableWidget()
        # 设置行数
        tableWidget.setRowCount(4)
        # 设置列数
        tableWidget.setColumnCount(3)

        # 把控件添加到布局里
        layout.addWidget(tableWidget)

        # 设水平表头
        tableWidget.setHorizontalHeaderLabels(["姓名","年龄","籍贯"])

        # 创建第一个QTableWidgetItem对象
        nameItem = QTableWidgetItem("小明")
        # 把nameItem放置在tablewidget里面
        # 放置在第一行第一列
        tableWidget.setItem(0,0,nameItem)

        # 创建第二个QTableWidgetItem对象
        ageItem = QTableWidgetItem("22")
        # 把nameItem放置在tablewidget里面
        # 放置在第一行第二列
        tableWidget.setItem(0, 1, ageItem)

        # 创建第三个QTableWidgetItem对象
        jiguanItem = QTableWidgetItem("天津")
        # 把nameItem放置在tablewidget里面
        # 放置在第一行第三列
        tableWidget.setItem(0, 2, jiguanItem)


        # 禁止编辑
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 让光标整行显示
        tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 调整列  根据内容调整
        tableWidget.resizeColumnsToContents()
        # 调整行  根据内容调整
        tableWidget.resizeRowsToContents()


        # 隐藏水平的头
        # tableWidget.horizontalHeader().setVisible(False)
        # 隐藏垂直的头
        # tableWidget.verticalHeader().setVisible(False)

        # 设置垂直的头
        tableWidget.setVerticalHeaderLabels(["a","b"])

        # 隐藏表格线
        tableWidget.setShowGrid(False)

        # 应用于水平布局
        self.setLayout(layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = TableWidgetDemo()
    example.show()
    sys.exit(app.exec_())
