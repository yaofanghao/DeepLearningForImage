# QLineEdit控件与回显模式
# QLineEdit控件的基本功能：1.输入单行的文本 2.设置回显模式EcoMode

"""
EcoMode(回显模式)
4种回显模式
1.Normal 正常的显示
2.Normal  不显示   类似于linux中输入密码没反应 但已经提交
3，Password  密码式的显示   类似于输入密码出现小黑点或*号
4，PasswordEchoOnEdit     密码显示编辑模式   常见于手机端，类似于  输入一个字母A,前两秒编辑框里显示的是A，过了一两秒编程框里变成的一个点或者*号
"""

import sys
from PyQt5.QtWidgets import *

# 从QWidget窗口类里面继承
class QLineEditEchoMode(QWidget):
    def __init__(self):
        super(QLineEditEchoMode,self).__init__()
        self.initUI()

    # 编写初始化方法
    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('文本输入框的回显模式')

        # 创建表单布局
        formLayout = QFormLayout()
        # 根据4种回显模式，分别创建4种表单布局

        # 第一种回显模式
        normalLineEdit = QLineEdit()
        # 第二种回显模式
        noEchoLineEdit = QLineEdit()
        # 第三种回显模式
        passwordLineEdit = QLineEdit()
        # 第四种回显模式
        passwordEchoONEditLineEdit = QLineEdit()

        # 把这四个控件添加到表单布局里面
        formLayout.addRow("Normal",normalLineEdit)
        formLayout.addRow("NoEcho",noEchoLineEdit)
        formLayout.addRow("Password",passwordLineEdit)
        formLayout.addRow("PasswordEchoOnEdit",passwordEchoONEditLineEdit)

        # 为每个文本框设置 placeholdertext ,就是当输入框没有输入时，以灰色字体显示这个文本框的提示
        normalLineEdit.setPlaceholderText("Normal")
        normalLineEdit.setPlaceholderText("NoEcho")
        passwordLineEdit.setPlaceholderText("Password")
        passwordEchoONEditLineEdit.setPlaceholderText("PasswprdEchoOnEdit")


        # 设置模式
        normalLineEdit.setEchoMode(QLineEdit.Normal)
        noEchoLineEdit.setEchoMode(QLineEdit.NoEcho)
        passwordLineEdit.setEchoMode(QLineEdit.Password)
        passwordEchoONEditLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        # 应用表单布局
        self.setLayout(formLayout)

# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QLineEditEchoMode()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())


