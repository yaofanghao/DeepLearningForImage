"""
显示打印对话框
"""

# 放置文本对话框，打开文档，显示页面设置对话框和打印文档对象框
import sys
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QTextEdit,QFileDialog,QDialog
from PyQt5.QtPrintSupport import QPageSetupDialog,QPrintDialog,QPrinter


class PrintDialog(QWidget):
    def __init__(self):
        super(PrintDialog, self).__init__()
        self.printer = QPrinter()
        self.initUI()

    def initUI(self):
        # 设置位置
        self.setGeometry(300,300,500,400)
        # 设置窗口标题
        self.setWindowTitle('打印对话框')

        # 创建文本框组件
        self.editor = QTextEdit(self)
        # 设置位置
        self.editor.setGeometry(20,20,300,270)

        # 创建button1控件
        # 打开按钮
        self.openButton = QPushButton('打开文件',self)
        # 设置位置
        self.openButton.move(350,20)

        # 创建button2控件
        # 设置按钮
        self.settingsButton = QPushButton('打印设置',self)
        # 设置位置
        self.settingsButton.move(350,50)

        # 创建button3控件
        # 打印按钮
        self.printButton = QPushButton('打印文档',self)
        # 设置位置
        self.printButton.move(350,80)


        # 绑定信号 槽
        self.openButton.clicked.connect(self.openFile)
        self.settingsButton.clicked.connect(self.showSettingDialog)
        self.printButton.clicked.connect(self.showPrintDialog)


    # 槽方法
    # 打开文件
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self,'打开文本文件','./')
        if fname[0]:
            with open(fname[0],'r',encoding='utf-8',errors='ignore') as f:
                self.editor.setText(f.read())

    # 显示打印设置对话框
    def showSettingDialog(self):
        printDialog = QPageSetupDialog(self.printer,self)
        printDialog.exec()

    # 显示打印对话框
    def showPrintDialog(self):
        printdialog = QPrintDialog(self.printer,self)
        if QDialog.Accepted == printdialog.exec():
            self.editor.print(self.printer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = PrintDialog()
    gui.show()
    sys.exit(app.exec_())
