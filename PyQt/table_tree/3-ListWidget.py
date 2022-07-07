"""
扩展的列表控件(QListWidget)
QListWidget是QListView的子类
支持MVC 和 VMC
"""
import sys
from PyQt5.QtWidgets import *


class ListWidgetDemo(QMainWindow):
    def __init__(self,parent= None):
        super(ListWidgetDemo, self).__init__(parent)
        # 设置窗口标题
        self.setWindowTitle('QListWidget 例子')
        # 设置窗口的尺寸
        self.resize(300,270)

        # 创建QListWidget控件
        self.listwidget = QListWidget()

        # 设置的尺寸
        # self.listwidget.resize(300,120)


        # 给QListWidget控件添加数据项
        self.listwidget.addItem("item1")
        self.listwidget.addItem("item2")
        self.listwidget.addItem("item3")
        self.listwidget.addItem("item4")
        self.listwidget.addItem("item5")

        # 给QListWidget控件设置标题
        self.listwidget.setWindowTitle("demo")
        # 设为中心窗口
        self.setCentralWidget(self.listwidget)

        # 连接信号 槽
        self.listwidget.itemClicked.connect(self.clicked)


    # 槽方法
    def clicked(self,Index):
        QMessageBox.information(self,"QListWidget","您选择了：" + self.listwidget.item(self.listwidget.row(Index)).text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ListWidgetDemo()
    win.show()
    sys.exit(app.exec_())
