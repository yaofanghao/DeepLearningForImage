"""
显示列表数据 (QListView控件)
"""

import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QListView,QMessageBox
from PyQt5.QtCore import QStringListModel

class ListViewDemo(QWidget):
    def __init__(self ,parent = None):
        super(ListViewDemo, self).__init__(parent)
        # 设置窗口标题
        self.setWindowTitle("QListView例子")
        # 设置窗口尺寸
        self.resize(300,270)



        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建QListView
        listview = QListView()

        # 创建字符串列表的模型
        # model相当于一个数据源
        listModel = QStringListModel()

        # 创建数据源
        self.list = ["列表项1","列表项2","列表项3"]

        # 把模型和列表绑定
        listModel.setStringList(self.list)
        listview.setModel(listModel)

        listview.clicked.connect(self.clicked)

        # 把控件添加到布局里
        layout.addWidget(listview)

        # 应用于垂直布局
        self.setLayout(layout)



    # 槽
    def clicked(self,item):
        QMessageBox.information(self,"QListView","您选择了：" + self.list[item.row()])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())

