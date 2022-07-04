"""
复选框控件(QCheckBox)
作用：同时可选中多个控件
复选框控件有三种状态：
未选中： 0
半选中： 1
选中：   2

"""
import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class QCheckBoxDemo(QWidget):
    def __init__(self):
        super(QCheckBoxDemo,self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('复选框控件演示')


        # 创建水平布局
        layout = QHBoxLayout()

        # 创建checkBox1复选框控件
        self.checkBox1 = QCheckBox('复选框控件1')
        #设置复选框默认为选中状态
        self.checkBox1.setChecked(True)


        # 创建checkBox2复选框控件
        # 普通控件，状态是未选中
        self.checkBox2 = QCheckBox('复选框控件2')

        # 创建checkBox3复选框控件 状态是半选中
        self.checkBox3 = QCheckBox('复选框控件3')
        # 处于半选中状态，需要下面两行代码
        self.checkBox3.setTristate(True)
        # 需要单独导Qt包   from PyQt5.QtCore import Qt
        self.checkBox3.setCheckState(Qt.PartiallyChecked)

        # 应用于水平布局
        self.setLayout(layout)

        # 将信号与槽绑定
        # 状态变化信号
        self.checkBox1.stateChanged.connect(lambda: self.checkboxState(self.checkBox1))
        self.checkBox2.stateChanged.connect(lambda: self.checkboxState(self.checkBox2))
        self.checkBox3.stateChanged.connect(lambda: self.checkboxState(self.checkBox3))

        # 把控件添加到水平布局里
        layout.addWidget(self.checkBox1)
        layout.addWidget(self.checkBox2)
        layout.addWidget(self.checkBox3)




    # 编写槽方法
    # 通过checkState可以设置三种状态
    def checkboxState(self,cb):
        check1Status = self.checkBox1.text() + ', isChecked=' + str(self.checkBox1.isChecked()) + ',checkState=' +str(self.checkBox1.checkState()) + '\n'
        check2Status = self.checkBox2.text() + ', isChecked=' + str(self.checkBox2.isChecked()) + ',checkState=' +str(self.checkBox2.checkState()) + '\n'
        check3Status = self.checkBox3.text() + ', isChecked=' + str(self.checkBox3.isChecked()) + ',checkState=' +str(self.checkBox3.checkState()) + '\n'
        print(check1Status + check2Status + check3Status)

# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QCheckBoxDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())
