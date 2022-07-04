"""
下拉列表控件

需要了解3点
1.如何将列表项添加到QComboBox控件中

2.如何获取选中的列表项

"""
import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class QComboBoxDemo(QWidget):
    def __init__(self):
        super(QComboBoxDemo,self).__init__()
        self.initUI()

    # 编写初始化方法
    def initUI(self):

        # 设置窗口标题
        self.setWindowTitle('下拉列表控件演示')
        # 设置窗口尺寸
        self.resize(300,100)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建label控件
        self.label = QLabel('请选择编程语言')
        # 创建QComboBox控件
        self.cb = QComboBox()
        # 用QComboBox里面的addItem添加
        self.cb.addItem('C++')
        self.cb.addItem('Python')
        # 也可以直接添加多个
        self.cb.addItems(['Java','Go','C','C#'])

        # 绑定信号和槽
        # currentIndexChanged 当前索引变化，从0开始
        self.cb.currentIndexChanged.connect(self.selectionChange)

        # 把控件添加到垂直布局里
        layout.addWidget(self.label)
        layout.addWidget(self.cb)

        # 应用于垂直布局
        self.setLayout(layout)

    # 槽方法
    # 默认传两个参数，一个是控件本身，一个是索引
    def selectionChange(self,i):
        # 得到当前选择的文本
        self.label.setText(self.cb.currentText())
        # 调整尺寸
        self.label.adjustSize()

        # 通过循环查看状态
        for count in range(self.cb.count()):
            # 根据索引，得到当前项的文本
            print('item' + str(count) + '=' + self.cb.itemText(count))
        print('current index',i,'selection changed',self.cb.currentText())

# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QComboBoxDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())



