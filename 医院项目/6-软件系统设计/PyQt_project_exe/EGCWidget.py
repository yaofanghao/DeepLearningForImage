# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EGCWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 700)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(136, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(119, 139, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(136, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(119, 139, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(119, 139, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        Form.setPalette(palette)
        Form.setAutoFillBackground(False)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(320, 20, 291, 50))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.pushButton6 = QtWidgets.QPushButton(Form)
        self.pushButton6.setGeometry(QtCore.QRect(630, 640, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton6.setFont(font)
        self.pushButton6.setStyleSheet("background-color: rgb(147, 149, 255);")
        self.pushButton6.setObjectName("pushButton6")
        self.pushButton7 = QtWidgets.QPushButton(Form)
        self.pushButton7.setGeometry(QtCore.QRect(440, 640, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton7.setFont(font)
        self.pushButton7.setStyleSheet("background-color: rgb(80, 170, 53);")
        self.pushButton7.setObjectName("pushButton7")
        self.pushButton8 = QtWidgets.QPushButton(Form)
        self.pushButton8.setGeometry(QtCore.QRect(820, 640, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton8.setFont(font)
        self.pushButton8.setStyleSheet("background-color: rgb(255, 170, 0);\n"
"color: rgb(0, 0, 255);")
        self.pushButton8.setObjectName("pushButton8")
        self.lineEdit2 = QtWidgets.QLineEdit(Form)
        self.lineEdit2.setGeometry(QtCore.QRect(130, 600, 101, 20))
        self.lineEdit2.setText("")
        self.lineEdit2.setObjectName("lineEdit2")
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(60, 600, 71, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.label4 = QtWidgets.QLabel(Form)
        self.label4.setGeometry(QtCore.QRect(50, 69, 101, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")
        self.label3 = QtWidgets.QLabel(Form)
        self.label3.setGeometry(QtCore.QRect(470, 69, 101, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.pushButton1 = QtWidgets.QPushButton(Form)
        self.pushButton1.setGeometry(QtCore.QRect(50, 530, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton1.setFont(font)
        self.pushButton1.setStyleSheet("background-color:rgb(85, 170, 255)")
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton5 = QtWidgets.QPushButton(Form)
        self.pushButton5.setGeometry(QtCore.QRect(770, 530, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton5.setFont(font)
        self.pushButton5.setStyleSheet("background-color: rgb(80, 170, 53);")
        self.pushButton5.setObjectName("pushButton5")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(0, 0, 1000, 700))
        self.listView.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.483, y1:0, x2:0.511727, y2:1, stop:0.5625 rgba(255, 229, 152, 255), stop:1 rgba(255, 255, 255, 255));")
        self.listView.setObjectName("listView")
        self.label5 = QtWidgets.QLabel(Form)
        self.label5.setGeometry(QtCore.QRect(50, 100, 400, 400))
        self.label5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label5.setText("")
        self.label5.setObjectName("label5")
        self.lineEdit5 = QtWidgets.QLineEdit(Form)
        self.lineEdit5.setGeometry(QtCore.QRect(400, 600, 121, 20))
        self.lineEdit5.setObjectName("lineEdit5")
        self.label6 = QtWidgets.QLabel(Form)
        self.label6.setGeometry(QtCore.QRect(460, 100, 400, 400))
        self.label6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label6.setText("")
        self.label6.setObjectName("label6")
        self.pushButton4 = QtWidgets.QPushButton(Form)
        self.pushButton4.setGeometry(QtCore.QRect(590, 530, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton4.setFont(font)
        self.pushButton4.setStyleSheet("background-color: rgb(80, 170, 53);")
        self.pushButton4.setObjectName("pushButton4")
        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(400, 530, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton2.setFont(font)
        self.pushButton2.setStyleSheet("background-color:rgb(85, 170, 255)")
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton3 = QtWidgets.QPushButton(Form)
        self.pushButton3.setGeometry(QtCore.QRect(230, 530, 141, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.pushButton3.setFont(font)
        self.pushButton3.setStyleSheet("background-color:rgb(85, 170, 255)")
        self.pushButton3.setObjectName("pushButton3")
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(590, 600, 101, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.lineEdit3 = QtWidgets.QLineEdit(Form)
        self.lineEdit3.setGeometry(QtCore.QRect(700, 600, 71, 20))
        self.lineEdit3.setText("")
        self.lineEdit3.setObjectName("lineEdit3")
        self.label7 = QtWidgets.QLabel(Form)
        self.label7.setGeometry(QtCore.QRect(310, 600, 81, 20))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        self.label7.setFont(font)
        self.label7.setObjectName("label7")
        self.listView.raise_()
        self.label.raise_()
        self.pushButton6.raise_()
        self.pushButton7.raise_()
        self.pushButton8.raise_()
        self.lineEdit2.raise_()
        self.label2.raise_()
        self.label4.raise_()
        self.label3.raise_()
        self.pushButton1.raise_()
        self.pushButton5.raise_()
        self.label5.raise_()
        self.lineEdit5.raise_()
        self.label6.raise_()
        self.pushButton4.raise_()
        self.pushButton2.raise_()
        self.pushButton3.raise_()
        self.label1.raise_()
        self.lineEdit3.raise_()
        self.label7.raise_()
        self.label2.setBuddy(self.lineEdit2)
        self.label5.setBuddy(self.lineEdit5)
        self.label6.setBuddy(self.lineEdit5)
        self.label1.setBuddy(self.lineEdit2)
        self.label7.setBuddy(self.lineEdit2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "EGC病变诊断"))
        self.label.setText(_translate("Form", "ME-NBI内镜图检测"))
        self.pushButton6.setText(_translate("Form", "返回诊断系统\n"
"选择页面"))
        self.pushButton7.setText(_translate("Form", "填写报告"))
        self.pushButton8.setText(_translate("Form", "退出检测"))
        self.label2.setText(_translate("Form", "日期"))
        self.label4.setText(_translate("Form", "图片显示"))
        self.label3.setText(_translate("Form", "预测结果"))
        self.pushButton1.setText(_translate("Form", "导入文件夹"))
        self.pushButton5.setText(_translate("Form", "显示诊断结果"))
        self.lineEdit5.setPlaceholderText(_translate("Form", "图片所在路径"))
        self.pushButton4.setText(_translate("Form", "开始检测"))
        self.pushButton2.setText(_translate("Form", "下一个"))
        self.pushButton3.setText(_translate("Form", "上一个"))
        self.label1.setText(_translate("Form", "预测置信度"))
        self.label7.setText(_translate("Form", "图片名称"))
