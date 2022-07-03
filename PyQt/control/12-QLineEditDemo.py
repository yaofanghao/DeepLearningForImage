# QLineEdit综合案例

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


# 创建一个类，从QWidget窗口类里面继承
class QLineEditDemo(QWidget):
    def __init__(self):
        super(QLineEditDemo,self).__init__()
        self.initUI()

    # 编写初始化方法
    def initUI(self):

        # 创建多个edit对象

        # 创建第一个控件
        edit1 = QLineEdit()
        # 使用int校验器
        edit1.setValidator(QIntValidator())
        # 设置文本框最大长度(位数)，即不超过9999
        edit1.setMaxLength(4)
        # 设置文本右对齐
        edit1.setAlignment(Qt.AlignRight)
        # 设置文本字体为Arial 字号 20
        edit1.setFont(QFont('Arial',20))



        # 创建第二个控件
        edit2 = QLineEdit()
        # 使用浮点校验器  范围0.99-99.99 精度为2
        edit2.setValidator(QDoubleValidator(0.99,99.99,2))
        # 未设置字体字号，对齐方式


        # 创建第三个控件
        edit3 = QLineEdit()
        # 使用掩码    掩码9表示 ：ASCⅡ数字字符是必须输入的(0-9)
        edit3.setInputMask('99_9999_999999;#')  # 后面'#'号指没有输入时，显示为'#'

       # 创建第四个控件
        edit4 = QLineEdit()
        # 绑定事件，当文本变化时，响应到槽
        edit4.textChanged.connect(self.textChanged)


        # 创建第五个控件
        edit5 = QLineEdit()
        # 设置回显模式
        edit5.setEchoMode(QLineEdit.Password)
        # 绑定事件，当编辑完成时，响应到槽
        edit5.editingFinished.connect(self.enterPress)


        # 创建第六个控件
        edit6 =QLineEdit()
        # 设为只读
        edit6.setReadOnly(True)



        # 创建表单布局
        formLayout = QFormLayout()

        # 把控件添加到表单里
        formLayout.addRow('整数校验',edit1)
        formLayout.addRow('浮点数校验',edit2)
        formLayout.addRow('Input Mask',edit3)
        formLayout.addRow('文本变化',edit4)
        formLayout.addRow('密码',edit5)
        formLayout.addRow('只读',edit6)

        # 应用于表单布局
        self.setLayout(formLayout)

        # 设置窗口的标题
        self.setWindowTitle('QLineEdit综合案例')



    # 当文本变化时，触发事件
    # 定义槽一
    def textChanged(self,text):
        print('输入的文本：' + text)

    # 定义槽二
    def enterPress(self):
        print('已输入值')
# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QLineEditDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())


