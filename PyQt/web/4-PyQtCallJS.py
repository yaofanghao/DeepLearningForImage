"""
PyQt5调用JavaScript代码

PyQt5和JavaScript交互
PyQt5和JavaScript互相调用，互相传输数据
"""

import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class PyQtCallJS(QWidget):
    def __init__(self):
        super(PyQtCallJS, self).__init__()
        self.setWindowTitle('PyQt5调用JavaScript')
        self.setGeometry(5,30,1355,730)
        # 设置垂直布局
        self.layout = QVBoxLayout()
        # 应用于垂直布局
        self.setLayout(self.layout)
        # 设置Web页面控件
        self.browser =  QWebEngineView()

        url = os.getcwd() + '/demo1.html'
        self.browser.load(QUrl.fromLocalFile(url))

        # 把web控件放到布局里
        self.layout.addWidget(self.browser)

        button = QPushButton('设置全名')
        self.layout.addWidget(button)

        # 槽和信号绑定
        button.clicked.connect(self.fullname)

    # 添加按钮的单击事件
    # 前两个框自己输入，最后一个框自动相加
    def fullname(self):
        self.value = 'hello world'
        self.browser.page().runJavaScript('fullname("' + self.value +'");',self.js_callback)

    # 通过回调函数返回值
    def js_callback(self,result):
        print(result)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PyQtCallJS()
    demo.show()
    sys.exit(app.exec_())
