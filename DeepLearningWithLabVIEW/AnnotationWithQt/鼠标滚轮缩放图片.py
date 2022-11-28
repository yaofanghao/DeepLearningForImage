# https://blog.csdn.net/qq_36780295/article/details/109034448

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import cv2.cv2 as cv

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.path = ""
        self.cur_img = ""
        self.img_w = ""
        self.img_h = ""
        self.resize_point = 10
        self.cur_resimg = ""

    def initUI(self):
        self.setGeometry(300, 200, 580, 430)
        self.setWindowTitle('Hello')

        self.pushbutton = QtWidgets.QPushButton(self)
        self.pushbutton.setGeometry(0, 0, 100, 30)
        self.pushbutton.clicked.connect(self.open_pic)
        self.pushbutton.setText("选择图片")

        self.groupbox = QtWidgets.QGroupBox(self)
        self.groupbox.setGeometry(0, 30, 580, 400)

        self.label = QtWidgets.QLabel(self.groupbox)
        self.label.setGeometry(0, 0, 580, 400)

    def open_pic(self):
        self.path = Qt.QFileDialog.getOpenFileName()
        self.cur_img = cv.imread(self.path[0])
        self.img_w = 580
        self.img_h = 400
        self.label.setPixmap(QtGui.QPixmap(self.path[0]).scaled(self.img_w, self.img_h))

    def wheelEvent(self, event):
        self.angle = event.angleDelta() / 8
        self.angleY = self.angle.y()
        if self.angleY > 0:
            if self.resize_point >= 1 and self.resize_point <= 19:
                self.resize_point += 1
        elif self.angleY < 0:
            if self.resize_point >= 2 and self.resize_point <= 20:
                self.resize_point -= 1
        self.cur_resimg = cv.resize(self.cur_img, (
        int(self.cur_img.shape[1] * self.resize_point / 10), int(self.cur_img.shape[0] * self.resize_point / 10)))
        img2 = cv.cvtColor(self.cur_resimg, cv.COLOR_BGR2RGB)
        QImage = QtGui.QImage(img2, self.cur_resimg.shape[1], self.cur_resimg.shape[0], 3 * self.cur_resimg.shape[1],
                              QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap(QImage).scaled(self.cur_resimg.shape[1], self.cur_resimg.shape[0])

        self.label_w = self.cur_resimg.shape[1]
        self.label_h = self.cur_resimg.shape[0]
        self.label.setGeometry(QtCore.QRect(int((1 - self.resize_point / 10) * self.cur_resimg.shape[1] / 2),
                                            int((1 - self.resize_point / 10) * self.cur_resimg.shape[0] / 2),
                                            self.label_w, self.label_h))
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

