"""
显示二维表数据(QTableView控件)

对于QTableView控件，它的数据源是Model

需要创建QTableView实例和一个数据源(Model),然后将两者关联
MVC：Model  Viewer  Controller
MVC的目的是将后端的数据和前端页面的耦合度降低


"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class TableView(QWidget):
    def __init__(self):
        super(TableView, self).__init__()
        # 设置窗口标题
        self.setWindowTitle("QTableView表格视图控件演示")
        # 设置窗口尺寸
        self.resize(500,300)
        # 创建QStandardItemModel对象  4行3列
        self.model = QStandardItemModel(4,3)
        # 设置字段
        self.model.setHorizontalHeaderLabels(['id','姓名','年龄'])

        # 创建QTableView控件
        self.tableview = QTableView()

        # 关联模型
        self.tableview.setModel(self.model)


        # 添加数据

        item11 = QStandardItem('10')
        itme12 = QStandardItem('杰克')
        item13 = QStandardItem('18')
        #  第一行第一列
        self.model.setItem(0,0,item11)
        #  第一行第二列
        self.model.setItem(0,1,itme12)
        #  第一行第三列
        self.model.setItem(0,2,item13)



        item31 = QStandardItem('99')
        itme32 = QStandardItem('酒桶')
        item33 = QStandardItem('21')
        #  第一行第一列
        self.model.setItem(2, 0, item31)
        #  第一行第二列
        self.model.setItem(2, 1, itme32)
        #  第一行第三列
        self.model.setItem(2, 2, item33)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 把控件添加到布局里
        layout.addWidget(self.tableview)

        # 应用于垂直布局
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = TableView()
    table.show()
    sys.exit(app.exec_())
