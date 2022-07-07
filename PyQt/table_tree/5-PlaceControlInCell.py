"""
在单元格放置控件
setItem：将文本放到单元格中
setCellWidget:将控件放到单元格
setStyleSheet:设置控件的样式(QSS)

"""
import sys
from PyQt5.QtWidgets import (QWidget,QTableWidget,QHBoxLayout,QApplication,QTableWidgetItem,QComboBox,QPushButton)


class PlaceControlInCell(QWidget):
    def __init__(self):
        super(PlaceControlInCell, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle("在单元格中放置控件")
        # 设置窗口尺寸
        self.resize(430,300)
        # 创建水平布局
        layout = QHBoxLayout()

        # 创建一个QTableWiddget控件
        tableWidget = QTableWidget()
        # 为QTableWiddget指定行
        tableWidget.setRowCount(4)
        # 为QTableWiddget指定列
        tableWidget.setColumnCount(3)

        # 把控件添加到布局里
        layout.addWidget(tableWidget)

        # 为 tableWidget 添加表格的头
        tableWidget.setHorizontalHeaderLabels(['姓名','性别','体重（kg）'])

        # 创建 QTableWidgetItem
        # 放置文本
        textItem = QTableWidgetItem('小明')

        # 把文本项添加到tablewidget里面
        # setItem 一般三个参数，行 列 传哪
        # 将这个文本放到第一行第一列
        tableWidget.setItem(0,0,textItem)


        # 创建QComboBox对象
        combox = QComboBox()
        # 给combox添加两个选项
        combox.addItem('男')
        combox.addItem('女')

        # QSS  类似于web里面的CSS  Qt StyleSheet
        # 设置所有的combox控件，让它的边距是3px
        combox.setStyleSheet('QComboBox{margin:3px};')
        # 在单元格放置控件
        # 防止第一行第二列
        tableWidget.setCellWidget(0,1,combox)

        # 创建一个button组件
        modifyButton = QPushButton('修改')
        # 默认是按下状态
        modifyButton.setDown(True)
        # 使用QSS设置样式  设置所有的QPushButton控件，让它的边距是3px
        modifyButton.setStyleSheet('QPushButton{margin:3px};')
        # 在单元格放置控件
        tableWidget.setCellWidget(0,2,modifyButton)

        # 应用于水平布局
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example  =PlaceControlInCell()
    example.show()
    sys.exit(app.exec_())
