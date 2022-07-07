"""
为树节点添加响应事件
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class TreeEvent(QMainWindow):
    def __init__(self,parent= None):
        super(TreeEvent, self).__init__(parent)
        self.setWindowTitle('为树节点添加响应事件')

        # 创建一个树
        self.tree = QTreeWidget()
        # 给这个树创建列的数量
        self.tree.setColumnCount(2)

        # 设置头
        # 指定列标签
        self.tree.setHeaderLabels(['Key','Value'])

        # 创建节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0,"root")
        root.setText(1,'0')

        # 创建子节点
        # 让子节点child1指向root
        child1 = QTreeWidgetItem(root)
        # 给子节点第一列设置文本
        child1.setText(0,"child1")
        # 给子节点第二列设置文本
        child1.setText(1,'1')

        # 创建子节点
        # 让子节点child2指向root
        child2 = QTreeWidgetItem(root)
        # 给子节点第一列设置文本
        child2.setText(0, "child2")
        # 给子节点第二列设置文本
        child2.setText(1, '2')

        # 创建子节点
        # 让子节点child3指向child2
        child3 = QTreeWidgetItem(child2)
        # 给子节点第一列设置文本
        child2.setText(0, "child3")
        # 给子节点第二列设置文本
        child2.setText(1, '3')


        # 将树设置为中心控件，充满整个屏幕
        # 这样在屏幕上就可以显示
        self.setCentralWidget(self.tree)

        # 为树添加节点，用单击信号
        self.tree.clicked.connect(self.onTreeClicked)

    # 槽方法
    def onTreeClicked(self,index):
        # 获得当前的单击项
        item = self.tree.currentItem()
        # 当前行
        print(index.row())
        # 输出当前单击节点的key
        print('key=%s,value=%s' % (item.text(0),item.text(1)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = TreeEvent()
    tree.show()
    sys.exit(app.exec_())
