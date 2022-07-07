"""
设置单元格的文本对齐方式

使用setTextAlignment方法
里面有一些常量  Qt.AlignRight  Qt.AlignBottom

"""
import sys
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem)
from PyQt5.QtCore import  Qt

class CellTextAlignment(QWidget):
    def __init__(self):
        super(CellTextAlignment, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('设置单元格的文本对齐方式')
        # 设置尺寸
        self.resize(430,230)
        # 创建水平布局
        layout = QHBoxLayout()

        # 创建QTableWidget控件
        tableWidget = QTableWidget()
        # 设置行数
        tableWidget.setRowCount(4)
        # 设置列数
        tableWidget.setColumnCount(3)

        # 把控件添加到布局里
        layout.addWidget(tableWidget)

        # 设置水平表头
        tableWidget.setHorizontalHeaderLabels(['姓名','性别','体重(kg)'])

        # 添加字段
        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('水生')
        # 设置文本为右对齐  默认单元格的顶端显示  可以设置为底端
        newItem.setTextAlignment(Qt.AlignRight | Qt.AlignBottom)
        # 给tableWidget添加newItem字段   此时表内是空的
        #  把newItem字段添加到第一行第一列
        tableWidget.setItem(0,0,newItem)

        # 添加字段
        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('28')
        # 设置文本为中心对齐  上下左右都对称    Qt.AlignBottom未起作用
        newItem.setTextAlignment(Qt.AlignCenter | Qt.AlignBottom)
        # 给tableWidget添加newItem字段   此时表内是空的
        #  把newItem字段添加到第一行第二列
        tableWidget.setItem(0, 1, newItem)

        # 添加字段
        # 创建QTableWidgetItem控件
        newItem = QTableWidgetItem('178')
        # 设置文本为右对齐
        newItem.setTextAlignment(Qt.AlignRight)
        # 给tableWidget添加newItem字段   此时表内是空的
        #  把newItem字段添加到第一行第三列
        tableWidget.setItem(0, 2, newItem)



        # 应用于水平布局
        self.setLayout(layout)

# 单独执行此脚本，才会运行下面的代码
if __name__ == '__main__':
    # app实例化，并传参
    app = QApplication(sys.argv)
    # 创建对象
    example = CellTextAlignment()
    # 创建窗口
    example.show()
    # 进入主循环，调用exit方法，确保主循环顺利退出
    sys.exit(app.exec_())
