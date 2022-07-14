"""
让程序定时关闭

QTimer.singleShot    在指定时间后只调用一次

"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


if __name__ == '__main__':
    app = QApplication(sys.argv)

    label =  QLabel("<font color=red size=140><b>Hello World,窗口在5秒后自动关闭！</b></font>")
    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    label.show()
    # 设置五秒
    QTimer.singleShot(5000,app.quit)

    sys.exit(app.exec_())
