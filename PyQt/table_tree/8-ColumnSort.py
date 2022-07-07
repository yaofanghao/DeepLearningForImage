"""
按列排序

1.按那一列排序
2.排序类型  升序或降序

sortItems(columnIdex,orderType)
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class ColumnSort(QWidget):
    def __init__(self):
        super(ColumnSort, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('按列排序')
        # 设置窗口尺寸
        self.resize(600,400)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建QTableWdiget控件
        self.tableWidget  = QTableWidget()
        # 设置行数
        self.tableWidget.setRowCount(4)
        # 设置列数
        self.tableWidget.setColumnCount(3)

        # 把控件添加到布局里
        layout.addWidget(self.tableWidget)

        # 设置水平表头
        self.tableWidget.setHorizontalHeaderLabels(['姓名','性别','体重(kg)'])

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('张三')
        # 添加到第一行第一列
        self.tableWidget.setItem(0,0,newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('男')
        # 添加到第一行第二列
        self.tableWidget.setItem(0, 1, newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('178')
        # 添加到第一行第三列
        self.tableWidget.setItem(0, 2, newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('李四')
        # 添加到第二行第一列
        self.tableWidget.setItem(1, 0, newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('男')
        # 添加到第二行第二列
        self.tableWidget.setItem(1, 1, newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('172')
        # 添加到第二行第三列
        self.tableWidget.setItem(1, 2, newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('花花')
        # 添加到第三行第一列
        self.tableWidget.setItem(2, 0, newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('女')
        # 添加到第三行第二列
        self.tableWidget.setItem(2, 1, newItem)

        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('168')
        # 添加到第三行第三列
        self.tableWidget.setItem(2, 2, newItem)

       # 添加button按钮
        self.button = QPushButton('排序')
        # 绑定 信号 槽
        self.button.clicked.connect(self.order)

       # 把控件放到布局里
        layout.addWidget(self.button)

       # 设置当前的排序类型   降序排列
        self.orderType = Qt.DescendingOrder

        # 应用于布局
        self.setLayout(layout)

    # 槽方法
    def order(self):
        # 如果当前排序是降序，则改为升序
        if self.orderType == Qt.DescendingOrder:
            self.orderType = Qt.AscendigOrder

        else:
            # 如果是升序，改成降序
            self.orderType = Qt.DescendingOrder
        # 排序
        self.tableWidget.sortItems(2,self.orderType)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ColumnSort()
    # 创建窗口
    main.show()
    # 创建主程序
    sys.exit(app.exec_())
