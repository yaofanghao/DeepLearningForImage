# QTextEdit控件

# QTextLine只能输入一行文本，输入多行文本用QTextEdit  常用功能：获得文本和设置文本，除了支持普通的文本，还支持富文本(改变颜色，设置尺寸)

import sys
from PyQt5.QtWidgets import *

# 编写一个类，从QWidget里面继承
class QTextEditDemo(QWidget):
    def __init__(self):
        super(QTextEditDemo,self).__init__()
        self.initUI()

    # 编写初始化方法 规范代码，初始化写在一个方法里
    def initUI(self):
        # 设置窗口的标题
        self.setWindowTitle('QTextEdit控件演示')

        # 设置窗口的尺寸
        self.resize(300,300)

        # 创建全局控件  为什么要创建去全局控件，在槽方法里需要调用
        self.textEdit = QTextEdit()
        # 创建全局按钮
        # 按钮一：显示文本
        # buttonText = QPushButton('显示文本')
        self.buttonText = QPushButton('显示文本')
        # 按钮二：显示HTML
        # buttonHTML = QPushButton('显示HTML')
        self.buttonHTML = QPushButton('显示HTML')
        # 按钮三：获取文本
        # buttonToText = QPushButton('获取文本')
        self.buttonToText = QPushButton('获取文本')
        # 按钮四：获取HTML
        # buttonToHTML = QPushButton('获取HTML')
        self.buttonToHTML = QPushButton('获取HTML')


        # 创建垂直布局
        layout = QVBoxLayout()


        # 把控件添加到垂直布局里面
        layout.addWidget(self.textEdit)
        # layout.addWidget(buttonText)
        # layout.addWidget(buttonHTML)
        layout.addWidget(self.buttonText)
        layout.addWidget(self.buttonHTML)
        layout.addWidget(self.buttonToText)
        layout.addWidget(self.buttonToHTML)

        # 应用于垂直布局
        self.setLayout(layout)


    # 把槽绑定到单击按钮信号上
    #     buttonText.clicked.connect(self.onClick_ButtonText)
    #     buttonHTML.clicked.connect(self.onClick_ButtonHTML)
        self.buttonText.clicked.connect(self.onClick_ButtonText)
        self.buttonHTML.clicked.connect(self.onClick_ButtonHTML)
        self.buttonToText.clicked.connect(self.onClick_ButtonToText)
        self.buttonToHTML.clicked.connect(self.onClick_ButtonToHTML)


    # 定义槽方法一
    def onClick_ButtonText(self):
        # 调用文本框设置普通文本
        self.textEdit.setPlainText('Hello World,世界你好吗？')

    # 定义槽方法二
    def onClick_ButtonHTML(self):
        # 调用文本框设置HTML(富文本)
        self.textEdit.setHtml('<font color="blue" size="5">Hello World</font>')

    # 定义获取模块的两个槽
    # 定义槽方法三
    def onClick_ButtonToText(self):
        # 调用文本框设置普通文本
        print(self.textEdit.toPlainText())

    # 定义槽方法四
    def onClick_ButtonToHTML(self):
        # 调用文本框设置HTML(富文本)
        print(self.textEdit.toHtml())

  # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)

    # 设置图标
    # app.setWindowIcon(QIcon('images/001.jpg'))

    # 创建对象
    main = QTextEditDemo()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())

