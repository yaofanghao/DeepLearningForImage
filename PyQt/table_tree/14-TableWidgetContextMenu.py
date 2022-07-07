"""
在表格中显示上下文

1.如何弹出菜单
2.如何在满足条件的情况下弹出菜单 QMenu.exec_


"""
# 特定单元格点击鼠标右键弹出菜单

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMenu,QPushButton,QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem,QHeaderView)


class TableWidgetContextMenu(QWidget):
    def __init__(self):
        super(TableWidgetContextMenu, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('在表格中显示上下文菜单')
        self.resize(500,300)

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建全局的表格控件
        self.tableWidget = QTableWidget()
        # 表格设置行
        self.tableWidget.setRowCount(5)
        # 表格设置列
        self.tableWidget.setColumnCount(3)

        # 把表格添加到水平布局里
        layout.addWidget(self.tableWidget)

        # 设置水平表格头
        self.tableWidget.setHorizontalHeaderLabels(['姓名','性别','体重'])

        # 添加字段
        newItem = QTableWidgetItem('张三')
        # 把字段添加到表格里 第一行第一列
        self.tableWidget.setItem(0,0,newItem)

        # 添加字段
        newItem = QTableWidgetItem('女')
        # 把字段添加到表格里  第一行第二列
        self.tableWidget.setItem(0, 1, newItem)

        # 添加字段
        newItem = QTableWidgetItem('28')
        # 把字段添加到表格里   第一行第三列
        self.tableWidget.setItem(0, 2, newItem)

        # 设置允许弹出菜单  单击右键响应事件
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # 将信号请求连接到一个槽
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        # 应用于水平布局
        self.setLayout(layout)

    # 槽方法
    def generateMenu(self,pos):
        # pos 为单击鼠标右键的坐标  相对于窗口
        # 鼠标右键单击前两行弹出菜单，单击第三行没响应
        print(pos)


        for i in self.tableWidget.selectionModel().selection().indexes():
            # 当前选中的行
            rowNum = i.row()
        # 如果选择的行索引小于2，弹出上下文菜单
        if rowNum < 2:
            menu = QMenu()
            item1 = menu.addAction("菜单项1")
            item2 = menu.addAction("菜单项2")
            item3 = menu.addAction("菜单项3")
            # 相对于窗口的坐标系转换为相对于屏幕的坐标系  映射到全局
            screePos = self.tableWidget.mapToGlobal(pos)
            print(screePos)
            # 被阻塞
            # action = menu.exec(pos)
            action = menu.exec(screePos)
            if action == item1:
                print('选择了第1个菜单项',self.tableWidget.item(rowNum,0).text(),
                                       self.tableWidget.item(rowNum,1).text(),
                                       self.tableWidget.item(rowNum,2).text())
            elif action == item1:
                print('选择了第2个菜单项',self.tableWidget.item(rowNum,0).text(),
                                       self.tableWidget.item(rowNum,1).text(),
                                       self.tableWidget.item(rowNum,2).text())

            elif action == item1:
                print('选择了第3个菜单项',self.tableWidget.item(rowNum,0).text(),
                                       self.tableWidget.item(rowNum,1).text(),
                                       self.tableWidget.item(rowNum,2).text())
            else:
                return
if __name__ == '__main__':
    app  = QApplication(sys.argv)
    main = TableWidgetContextMenu()
    main.show()
    sys.exit(app.exec_())
