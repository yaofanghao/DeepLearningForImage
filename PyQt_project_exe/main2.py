import sys

from PyQt5 import QtCore,QtWidgets,QtGui

class Test():

    def setUI(self,w):

        #设置工具窗口的大小，前两个参数决定窗口的位置

        w.setGeometry(300,300,400,200)

        #设置工具窗口的标题

        # w.setWindowTitle("Test")

        #设置窗口的图标

        w.setWindowIcon(QtGui.QIcon('x.jpg'))

        # 添加文本标签

        self.label = QtWidgets.QLabel(w)

        # 设置标签的左边距，上边距，宽，高

        self.label.setGeometry(QtCore.QRect(60, 20, 120, 45))

        # 设置文本标签的字体和大小，粗细等

        self.label.setFont(QtGui.QFont("Roman times",20))

        self.label.setText("Name:")

        #添加设置一个文本框

        self.text = QtWidgets.QLineEdit(w)

        #调整文本框的位置大小

        self.text.setGeometry(QtCore.QRect(150,30,180,30))

        #第二个文本框的设置，同上，注意位置参数



        self.label_2 = QtWidgets.QLabel(w)

        self.label_2.setGeometry(QtCore.QRect(60, 70, 120, 45))

        self.label_2.setFont(QtGui.QFont("Roman times",20))

        self.label_2.setText("Phone:")

        self.text_2 = QtWidgets.QLineEdit(w)

        self.text_2.setGeometry(QtCore.QRect(150,80,180,30))

        #添加提交按钮和单击事件

        self.btn = QtWidgets.QPushButton(w)

        #设置按钮的位置大小

        self.btn.setGeometry(QtCore.QRect(150,140,70,30))

        #设置按钮的位置，x坐标,y坐标

        self.btn.move(150,140)

        self.btn.setText("提交")

        #为按钮添加单击事件

        self.btn.clicked.connect(self.getText)

        # 按钮点下后自动关闭当前界面

        self.btn.clicked.connect(w.close)

        w.show()

    def getText(self):

         name = self.text.text()

         phone = self.text_2.text()

         print(name,phone)

if __name__=='__main__':

    #创建应用程序和对象

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()

    ui = Test()

    ui.setUI(w)

    sys.exit(app.exec_())