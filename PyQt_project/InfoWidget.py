# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InfoWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 600)
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
        self.label.setGeometry(QtCore.QRect(330, 40, 201, 50))
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(90, 100, 701, 91))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.horizontalLayout.addWidget(self.label1)
        self.lineEdit1 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit1.setPlaceholderText("")
        self.lineEdit1.setObjectName("lineEdit1")
        self.horizontalLayout.addWidget(self.lineEdit1)
        self.label2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.horizontalLayout.addWidget(self.label2)
        self.lineEdit2 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit2.setPlaceholderText("")
        self.lineEdit2.setObjectName("lineEdit2")
        self.horizontalLayout.addWidget(self.lineEdit2)
        self.label3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.horizontalLayout.addWidget(self.label3)
        self.lineEdit3 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit3.setPlaceholderText("")
        self.lineEdit3.setObjectName("lineEdit3")
        self.horizontalLayout.addWidget(self.lineEdit3)
        self.label4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")
        self.horizontalLayout.addWidget(self.label4)
        self.lineEdit4 = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit4.setPlaceholderText("")
        self.lineEdit4.setObjectName("lineEdit4")
        self.horizontalLayout.addWidget(self.lineEdit4)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(90, 210, 701, 181))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit6 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit6.setPlaceholderText("")
        self.lineEdit6.setObjectName("lineEdit6")
        self.gridLayout.addWidget(self.lineEdit6, 0, 3, 1, 1)
        self.label5 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label5.setFont(font)
        self.label5.setObjectName("label5")
        self.gridLayout.addWidget(self.label5, 0, 0, 1, 1)
        self.label6 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label6.setFont(font)
        self.label6.setObjectName("label6")
        self.gridLayout.addWidget(self.label6, 0, 2, 1, 1)
        self.lineEdit5 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit5.setPlaceholderText("")
        self.lineEdit5.setObjectName("lineEdit5")
        self.gridLayout.addWidget(self.lineEdit5, 0, 1, 1, 1)
        self.label7 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label7.setFont(font)
        self.label7.setObjectName("label7")
        self.gridLayout.addWidget(self.label7, 0, 4, 1, 1)
        self.lineEdit7 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit7.setPlaceholderText("")
        self.lineEdit7.setObjectName("lineEdit7")
        self.gridLayout.addWidget(self.lineEdit7, 0, 5, 1, 1)
        self.label8 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label8.setFont(font)
        self.label8.setObjectName("label8")
        self.gridLayout.addWidget(self.label8, 1, 0, 1, 1)
        self.label9 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label9.setFont(font)
        self.label9.setObjectName("label9")
        self.gridLayout.addWidget(self.label9, 1, 2, 1, 1)
        self.lineEdit9 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit9.setPlaceholderText("")
        self.lineEdit9.setObjectName("lineEdit9")
        self.gridLayout.addWidget(self.lineEdit9, 1, 3, 1, 1)
        self.label10 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.label10.setFont(font)
        self.label10.setObjectName("label10")
        self.gridLayout.addWidget(self.label10, 1, 4, 1, 1)
        self.lineEdit10 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit10.setPlaceholderText("")
        self.lineEdit10.setObjectName("lineEdit10")
        self.gridLayout.addWidget(self.lineEdit10, 1, 5, 1, 1)
        self.lineEdit8 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit8.setPlaceholderText("")
        self.lineEdit8.setObjectName("lineEdit8")
        self.gridLayout.addWidget(self.lineEdit8, 1, 1, 1, 1)
        self.labelresult = QtWidgets.QLabel(Form)
        self.labelresult.setGeometry(QtCore.QRect(90, 410, 171, 20))
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(16)
        self.labelresult.setFont(font)
        self.labelresult.setObjectName("labelresult")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(90, 440, 531, 81))
        self.textEdit.setObjectName("textEdit")
        self.pushButton1 = QtWidgets.QPushButton(Form)
        self.pushButton1.setGeometry(QtCore.QRect(120, 530, 141, 51))
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.pushButton1.setFont(font)
        self.pushButton1.setStyleSheet("background-color: rgb(147, 149, 255);")
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(280, 530, 141, 51))
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.pushButton2.setFont(font)
        self.pushButton2.setStyleSheet("background-color: rgb(80, 170, 53);")
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton3 = QtWidgets.QPushButton(Form)
        self.pushButton3.setGeometry(QtCore.QRect(440, 530, 141, 51))
        font = QtGui.QFont()
        font.setFamily("??????")
        font.setPointSize(12)
        self.pushButton3.setFont(font)
        self.pushButton3.setStyleSheet("background-color:rgb(85, 170, 255)")
        self.pushButton3.setObjectName("pushButton3")
        self.listView = QtWidgets.QListView(Form)
        self.listView.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.listView.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.483, y1:0, x2:0.511727, y2:1, stop:0.5625 rgba(255, 229, 152, 255), stop:1 rgba(255, 255, 255, 255));")
        self.listView.setObjectName("listView")
        self.listView.raise_()
        self.label.raise_()
        self.horizontalLayoutWidget.raise_()
        self.gridLayoutWidget.raise_()
        self.labelresult.raise_()
        self.textEdit.raise_()
        self.pushButton1.raise_()
        self.pushButton2.raise_()
        self.pushButton3.raise_()
        self.label1.setBuddy(self.lineEdit1)
        self.label2.setBuddy(self.lineEdit2)
        self.label3.setBuddy(self.lineEdit3)
        self.label4.setBuddy(self.lineEdit4)
        self.label5.setBuddy(self.lineEdit5)
        self.label6.setBuddy(self.lineEdit6)
        self.label7.setBuddy(self.lineEdit7)
        self.label9.setBuddy(self.lineEdit9)
        self.label10.setBuddy(self.lineEdit10)
        self.labelresult.setBuddy(self.textEdit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "??????????????????"))
        self.label.setText(_translate("Form", "??????????????????"))
        self.label1.setText(_translate("Form", "?????????"))
        self.lineEdit1.setText(_translate("Form", "1"))
        self.label2.setText(_translate("Form", "?????????"))
        self.lineEdit2.setText(_translate("Form", "2"))
        self.label3.setText(_translate("Form", "?????????"))
        self.lineEdit3.setText(_translate("Form", "33"))
        self.label4.setText(_translate("Form", "?????????"))
        self.lineEdit4.setText(_translate("Form", "44"))
        self.lineEdit6.setText(_translate("Form", "???"))
        self.label5.setText(_translate("Form", "??????"))
        self.label6.setText(_translate("Form", "??????"))
        self.lineEdit5.setText(_translate("Form", "??????123"))
        self.label7.setText(_translate("Form", "??????"))
        self.lineEdit7.setText(_translate("Form", "12"))
        self.label8.setText(_translate("Form", "??????"))
        self.label9.setText(_translate("Form", "??????"))
        self.lineEdit9.setText(_translate("Form", "abc123"))
        self.label10.setText(_translate("Form", "??????"))
        self.lineEdit10.setText(_translate("Form", "123??????"))
        self.lineEdit8.setText(_translate("Form", "abc123???"))
        self.labelresult.setText(_translate("Form", "?????????????????????"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">123</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">test</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">abc</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">??????</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">end</p></body></html>"))
        self.pushButton1.setText(_translate("Form", "??????????????????\n"
"????????????"))
        self.pushButton2.setText(_translate("Form", "??????????????????"))
        self.pushButton3.setText(_translate("Form", "??????????????????"))
