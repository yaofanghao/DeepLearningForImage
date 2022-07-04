"""
字体对话框 QFontDialog

用来显示字体列表，并且选择某一个字体字号，然后返回
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class QFontDialogDemo(QWidget):
    def  __init__(self):
        super(QFontDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('FontDialog演示')
        # 设置窗口尺寸
        self.resize(300,100)

        # 创建一个垂直布局
        layout = QVBoxLayout()

        # 创建button控件
        self.fontButton = QPushButton('选择字体')

        # 创建label控件，用于接收设置的文本输入框
        self.fontLabel = QLabel('Hello,测试字体例子')

        # 绑定信号和槽
        self.fontButton.clicked.connect(self.getFont)

        # 把控件添加到布局里
        layout.addWidget(self.fontButton)
        layout.addWidget(self.fontLabel)

        # 应用于垂直布局
        self.setLayout(layout)

    # 槽方法
    def getFont(self):
        # 返回font对象，探测是否点ok或者cancel
        # getFont返回两个值
        font, ok = QFontDialog.getFont()
        if ok:
            self.fontLabel.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QFontDialogDemo()
    main.show()
    sys.exit(app.exec_())
