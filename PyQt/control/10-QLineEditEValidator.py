# 限制QLineEdit控件的输入(校验器)   只能输入满足格式的数据
# 如限制只能输入整数、浮点数或满足一定条件的字符串

# 本次演示做三种限制： 1.整数  2.浮点数   3.字母或者数字

import sys
from PyQt5.QtWidgets import *
# 导入PyQt5的正则(三个校验器，第三个可自定义)
from PyQt5.QtGui import QIntValidator,QDoubleValidator,QRegExpValidator
# 导入PyQt5里正则表达式的一个类QRegExp
from PyQt5.QtCore import QRegExp


# 编写一个类，从QWidget窗口类里面继承

class QLineEditValidator(QWidget):
    def __init__(self):
        super(QLineEditValidator,self).__init__()
        self.initUI()

    # 编写初始化方法
    def initUI(self):
        # 设置一下窗口标题
        self.setWindowTitle('校验器')

        # 创建表单布局
        formLayout = QFormLayout()

        # 创建三个文本输入框
        intLineEdit = QLineEdit()
        doubleLineEdit = QLineEdit()
        validatorLineEdit = QLineEdit()


        # 将这三个控件添加到form表单布局里
        formLayout.addRow('整数类型',intLineEdit)
        formLayout.addRow('浮点类型',doubleLineEdit)
        formLayout.addRow('数字和字母',validatorLineEdit)

        # 为每个文本框设置placeholdertext,就是当输入框没有输入时，以灰色字体显示这个文本框的提示
        intLineEdit.setPlaceholderText('整数')
        doubleLineEdit.setPlaceholderText('浮点型')
        validatorLineEdit.setPlaceholderText('字母和数字')

        # 创建整数校验器
        inValidator = QIntValidator(self)
        # 设置整数的范围 [1,99]
        inValidator.setRange(1,99)

        # 创建浮点校验器
        doubleValidator = QDoubleValidator(self)
        # 设置浮点校验器[-360,360]
        doubleValidator.setRange(-360,-360)
        # 小数点的表示
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)
        # 设置精度，小数点2位
        doubleValidator.setDecimals(2)

        # 创建数字和字母的正则表达式
        reg = QRegExp('[a-zA-Z0-9]+$')   # 此时+表示至少有一个
        # 创建数字和字母的校验器
        validator = QRegExpValidator(self)
        # 将正则表达式放置在校验器内
        validator.setRegExp(reg)


        # 设置校验器
        intLineEdit.setValidator(inValidator)
        doubleLineEdit.setValidator(doubleValidator)
        validatorLineEdit.setValidator(validator)


        # 应用表单布局
        self.setLayout(formLayout)


# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = QLineEditValidator()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())


