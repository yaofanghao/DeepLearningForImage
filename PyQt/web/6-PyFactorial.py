"""
JavaScript调用Python函数计算阶乘

基本原理
将Python的对象映射到JavaScript中，
通过映射到JavaScript的对象，来调用Python对象的方法或者函数

将槽函数映射到JavaScript中

在Python类中定义若干个槽函数
系统就会把槽函数连同JavaScript对象一起映射到JavaScript里面


调用JS，都是采用异步的方式 加一个回调  window.obj.factorial(n,callback)

"""

import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebChannel import QWebChannel

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from web.factorial import *

channel =QWebChannel()
factorial = Factorial()

class PyFactorial(QWidget):
    def __init__(self):
        super(PyFactorial, self).__init__()
        self.setWindowTitle('Python计算阶乘')
        self.resize(600,300)
        layout = QVBoxLayout()


        self.browser = QWebEngineView()
        url = os.getcwd() + '/h.html'
        self.browser.load(QUrl.fromLocalFile(url))
        channel.registerObject("obj",factorial)
        self.browser.page().setWebChannel(channel)

        layout.addWidget(self.browser)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PyFactorial()
    demo.show()
    sys.exit(app.exec_())

