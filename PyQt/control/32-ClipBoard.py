"""
使用剪贴板
"""
import sys,math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ClipBoard(QDialog):
    def __init__(self):
        super(ClipBoard, self).__init__()

        # 创建6个按钮组件
        textCopyButton = QPushButton('复制文本')
        textPasteButton = QPushButton('粘贴文本')

        htmlCopyButton = QPushButton('复制HTML')
        htmlPasteButton = QPushButton('粘贴HTML')

        imageCopyButton = QPushButton('复制图像')
        imagePasteButton = QPushButton('粘贴图像')

        #  创建两个label控件，一个用来显示粘贴的文本   一个用来显示图像
        self.textLabel = QLabel('默认文本')
        self.imageLabel = QLabel('显示头像')
        self.imageLabel.setPixmap(QPixmap('../controls/images/5.png'))

        # 设置栅格布局
        layout = QGridLayout()

        # 把控件添加到布局里
        # 第一行第一列
        layout.addWidget(textCopyButton,0,0)
        # 第一行第二列
        layout.addWidget(imageCopyButton,0,1)
        #第一行第三列
        layout.addWidget(htmlCopyButton,0,2)
        # 第二行第一列
        layout.addWidget(textPasteButton,1,0)
        # 第二行第二列
        layout.addWidget(htmlPasteButton,1,1)
        # 第二行第三列
        layout.addWidget(imagePasteButton,1,2)
        # 第三行第一列   占一行占两列
        layout.addWidget(self.textLabel,2,0,1,2)
        # 第三行第三列
        layout.addWidget(self.imageLabel,2,2)

        # 应用于栅格布局
        self.setLayout(layout)

        # 绑定信号  槽
        # 分别为这六个按钮指定单击事件
        # 复制文本
        textCopyButton.clicked.connect(self.copyText)
        # 粘贴文本
        textPasteButton.clicked.connect(self.pasteText)
        # 复制HTML
        htmlCopyButton.clicked.connect(self.copyHtml)
        # 粘贴HTML
        htmlPasteButton.clicked.connect(self.pasteHtml)
        # 复制图像
        imageCopyButton.clicked.connect(self.copyImage)
        # 粘贴图像
        imagePasteButton.clicked.connect(self.pasteImage)

        # 设置窗口标题
        self.setWindowTitle('剪贴板演示')

    # 槽方法
    def copyText(self):
        # 设置剪切板
        clipboard = QApplication.clipboard()
        # 设置剪切板内容
        clipboard.setText('hello world')

    def pasteText(self):
        # 设置剪切板
        clipboard = QApplication.clipboard()
        # 设置剪切板内容
        # 把剪切板的内容直接放到label里
        self.textLabel.setText(clipboard.text())

    def copyHtml(self):
        # 获取数据类型
        mimeData = QMimeData()
        # 设置HTML
        mimeData.setHtml('<b>Bold and <font color=red>Red</font></b>')
        # 获得剪切板
        clipborad = QApplication.clipboard()
        # 在剪切板设置数据
        clipborad.setMimeData(mimeData)

    def pasteHtml(self):
        # 获得剪切板
        clipboard = QApplication.clipboard()
        # 获得数据
        mimeData  = clipboard.mimeData()
        # 如果数据是html类型
        if mimeData.hasHtml():
            # 把html数据放在剪切板上
            self.textLabel.setText(mimeData.html())
    def copyImage(self):
        # 设置剪切板
        clipboard = QApplication.clipboard()
        # 设置剪切板内容
        clipboard.setPixmap(QPixmap('../controls/images/5.png'))
    def pasteImage(self):
        # 设置剪切板
        clipboard = QApplication.clipboard()
        # 设置剪切板的内容
        # 把剪切板的内容直接放到label里
        self.imageLabel.setPixmap(clipboard.pixmap())

# 防止其他脚本调用，只有单独运行此脚本，才会调用下面代码
if __name__ == '__main__':
    # app实例，并传参
    app = QApplication(sys.argv)
    # 创建对象
    main = ClipBoard()
    # 创建窗口
    main.show()
    # 执行主循环，调用exit方法，确保主循环安全退出
    sys.exit(app.exec_())
