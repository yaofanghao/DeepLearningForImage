"""
用Web浏览器控件(QWebEngineView)显示网页
PyQt5和Web的交互技术

同时使用Python和web开发程序，混合开发
Python + JavaScript + HTML5 + CSS

QWebEngineView 控件，用来显示Web交互界面

"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class WebEngineView(QMainWindow):

    def __init__(self):
        super(WebEngineView, self).__init__()
        self.setWindowTitle('打开外部网页例子')
        # 在距屏幕宽5px,高30px的坐标，创建一个宽1355，高730的窗口
        self.setGeometry(5,30,1355,730)

        self.browser = QWebEngineView()
        self.browser.load(QUrl('https://www.baidu.com/'))
        self.setCentralWidget(self.browser)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WebEngineView()
    win.show()
    sys.exit(app.exec_())
