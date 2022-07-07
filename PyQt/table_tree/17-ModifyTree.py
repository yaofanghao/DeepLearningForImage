"""
添加、修改和删除树控件中的节点
"""

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ModifyTree(QWidget):
    def __init__(self,parent=None):
        super(ModifyTree, self).__init__(parent)
        self.setWindowTitle('TreeWidget  例子')
        self.resize(600,400)

        operatorLayout = QHBoxLayout()
        # 创建按钮控件
        addBtn = QPushButton('添加节点')
        updateBtn = QPushButton('修改节点')
        deleteBtn = QPushButton('删除节点')


        # 把控件添加到水平布局里
        operatorLayout.addWidget(addBtn)
        operatorLayout.addWidget(updateBtn)
        operatorLayout.addWidget(deleteBtn)

        # 把这三个按钮绑定到相应的槽上
        addBtn.clicked.connect(self.addNode)
        updateBtn.clicked.connect(self.updateNode)
        deleteBtn.clicked.connect(self.deleteNode)

        #  下行代码不需要，一次应用于布局就可以了
        # self.setLayout(operatorLayout)
        # 创建一个树
        self.tree = QTreeWidget()
        # 给这个树创建列的数量
        self.tree.setColumnCount(2)

        # 设置头
        # 指定列标签
        self.tree.setHeaderLabels(['Key', 'Value'])
        #
        # 创建节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, "root")
        root.setText(1, '0')

        # 创建子节点
        # 让子节点child1指向root
        child1 = QTreeWidgetItem(root)
        # 给子节点第一列设置文本
        child1.setText(0, "child1")
        # 给子节点第二列设置文本
        child1.setText(1, '1')

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
        # self.setCentralWidget(self.tree)

        # 为树添加节点，用单击信号
        self.tree.clicked.connect(self.onTreeClicked)
        # 创建垂直布局
        mainLayout = QVBoxLayout(self)
        # 把按钮和树都放在垂直布局里
        # 此时按钮在水平布局里面
        mainLayout.addLayout(operatorLayout)
        # # 添加控件
        mainLayout.addWidget(self.tree)

        # 应用于垂直布局
        # self.setLayout(mainLayout)

    # 槽方法
    def onTreeClicked(self, index):
        # 获得当前的单击项
        item = self.tree.currentItem()
        # 当前行
        print(index.row())
        # 输出当前单击节点的key
        print('key=%s,value=%s' % (item.text(0), item.text(1)))

    # 槽方法
    def addNode(self):
        print('添加节点')
        # 获得当前的节点
        item = self.tree.currentItem()
        print(item)
        # 动态创建节点，指定父节点
        node = QTreeWidgetItem(item)
        # 创建node的第一列
        node.setText(0,'新节点')
        node.setText(1,'新值')
        # 创建node的第二列

    def updateNode(self):
        print('修改节点')
        # 获得当前的节点
        item = self.tree.currentItem()
        item.setText(0,'修改节点')
        item.setText(1,'值已经被修改')

    def deleteNode(self):
        print('删除节点')
        # 获得当前的节点
        item = self.tree.currentItem()
        # 通过循环  得到当前选中的节点
        # 获得不可见的根
        root = self.tree.invisibleRootItem()
        for item in self.tree.selectedItems():
            #  item.parent()和root只要有一个不为空，就不会出错
            (item.parent() or root).removeChild(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ModifyTree()
    main.show()
    sys.exit(app.exec_())
