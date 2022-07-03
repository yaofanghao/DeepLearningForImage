# QLabel与伙伴控件
# 1.通过setBuddy设置伙伴关系
# 2.通过栅格布局来完成手动布局，依靠
# mainLayout.addWidget(控件对象,rowIndex,columnIndex,row,column)   （行索引,索引,占用多少行,占用多少列）


import sys
from PyQt5.QtWidgets import *

class QLabelBuddy(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    # 规范代码，初始化直接写在一个方法里
    def initUI(self):
        # 设置主窗口的标题
        self.setWindowTitle('QLabel与伙伴控件')


        # 创建nameLabel控件
        #添加热键   添加热键的方法& + 英文字母  ，后面的英文字母就变成了热键。在可视化窗口里通过 "Alt" + 英文字母 就可以起作用
        nameLabel =QLabel('&Name',self)

        # 创建QLineEdit控件
        nameLineEdit = QLineEdit(self)

        # 把nameLabel和nameLineEdit设置伙伴关系
        nameLabel.setBuddy(nameLineEdit)

        # 创建PasswordQLabel控件, 并添加热键
        passwordLabel = QLabel('&Password',self)
        # 创建PasswordLineEdit控件
        passwordLineEdit = QLineEdit(self)

        # 把passwordLabel和passwordLineEdit设置成伙伴关系
        passwordLabel.setBuddy(passwordLineEdit)

        # 创建两个按钮，一个上面写OK,一个上面写Cancel
        btnOK = QPushButton('&OK')
        btnCancel = QPushButton('&Cancel')

        # 使用栅格布局
        mainLayout = QGridLayout(self)
        # 将nameLabel控件放到布局里面    第一行第一列
        mainLayout.addWidget(nameLabel,0,0)
        # 将nameLineEdit控件放到布局里面  第一行第二列，占用一行两列
        mainLayout.addWidget(nameLineEdit,0,1,1,2)
        # 将passwordLabel控件放到布局里面  第二行第一列
        mainLayout.addWidget(passwordLabel,1,0)
        # 将passwordLineEdit控件放到布局里面 第二行第一列，占用一行两列
        mainLayout.addWidget(passwordLineEdit,1,1,1,2)
        # 经过上面操作，此时有两行，每行有三列


        # 放置按钮  第三行第二列
        mainLayout.addWidget(btnOK,2,1)
        # 放置按钮    第三行第三列
        mainLayout.addWidget(btnCancel,2,2)

# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QLabelBuddy()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())


