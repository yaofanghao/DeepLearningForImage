"""
显示嵌入Web页面
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class InnerHTML(QMainWindow):
    def __init__(self):
        super(InnerHTML, self).__init__()
        self.setWindowTitle('显示嵌入Web页面')
        self.setGeometry(5,30,1355,730)
        self.browsesr = QWebEngineView()
        self.browsesr.setHtml(
            """
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>测试显示</title>
</head>
<body>
    <h1>Hello PyQt5!</h1>
    <div>显示Web页面</div>
    <spam>幸苦了</spam>
</body>
</html>          
            """
        )
        # 设置成中心控件
        self.setCentralWidget(self.browsesr)

if __name__ == '__main__':
    app =QApplication(sys.argv)
    demo = InnerHTML()
    demo.show()
    sys.exit(app.exec_())

