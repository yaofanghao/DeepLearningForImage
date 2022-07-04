"""
输入对话框：QInputDialog
提供了若干个静态方法
QInputDialog.getItem  用来显示输入列表
QInputDialog.getText   用来显示录入文本
QInputDialog.getInt    用来显示输入整数的  计数器控件

"""
import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *

class QInputDialogDemo(QWidget):
    def __init__(self):
        super(QInputDialogDemo, self).__init__()
        self.initUI()

    # 编写初始化方法
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('输入对话框')
        # 设置窗口尺寸
        self.resize(400,400)

        # 创建form表单布局
        layout = QFormLayout()

        # 创建button1控件
        self.button1 = QPushButton('获取列表中的选项')

        # 创建lineEdit1控件，放置在button1的右侧  在布局添加的时候设置
        self.lineEdit1 = QLineEdit()

        # 创建button2控件
        self.button2 = QPushButton('获取字符串')

        # 创建lineEdit2控件，放置在button2的右侧 在布局添加的时候设置
        self.lineEdit2 = QLineEdit()

        # 创建button3、lineEdit3控件
        self.button3 = QPushButton('获取整数')
        self.lineEdit3 = QLineEdit()

        # 绑定信号 槽
        self.button1.clicked.connect(self.getItem)
        self.button2.clicked.connect(self.getText)
        self.button3.clicked.connect(self.getInt)

        # 把控件添加到form表单布局里
        layout.addRow(self.button1,self.lineEdit1)
        layout.addRow(self.button2, self.lineEdit2)
        layout.addRow(self.button3, self.lineEdit3)

        # 应用于form表单布局
        self.setLayout(layout)

     # 槽方法
    def getItem(self):
        # 定义一个元组
        items =('C','C++','Ruby','Python','Java')
        item,ok = QInputDialog.getItem(self,'请选择编程语言','语言列表',items)
        if ok and item:
            self.lineEdit1.setText(item)
    def getText(self):
        text, ok = QInputDialog.getText(self,'文本输入框','输入姓名')
        if ok and text:
            self.lineEdit2.setText(text)
    def getInt(self):
        num, ok = QInputDialog.getInt(self,'整数输入框','输入数字')
        if ok and num:
            self.lineEdit3.setText(str(num))
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QInputDialogDemo()
    main.show()
    sys.exit(app.exec_())

