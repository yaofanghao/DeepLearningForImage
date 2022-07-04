"""
对话框的基类QDialog
在基类基础上有五种对话框
QMessageBox 消息对话框
QColorDialog 颜色对话框
QFileDialog  显示文件打开或保存对话框
QFontDialog  设置字体对话框
QInputDialog  输入信息对话框

回顾：
PyQt5的三种窗口
QMainWindow  主窗口
QWidget  不确定窗口的用途时
QDialog  没有菜单的窗口，一个对话框

"""
# 如何在主窗口里面显示对话框
import sys
# QtCore是Qt的精髓（包括五大模块：元对象系统，属性系统，对象模型，对象树，信号槽）
from PyQt5.QtCore import *
# QtGui 显示应用程序图标，工具提示和各种鼠标光标。
from PyQt5.QtGui import *
# Qt Widgets模块提供了一组UI元素来创建经典的桌面风格的用户界面。
from PyQt5.QtWidgets import *

class QDialogDemo(QMainWindow):
    def __init__(self):
        super(QDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle('QDialog案例')
        # 设置窗口尺寸
        self.resize(300,200)

        # 创建button控件，直接把button放在窗口上
        self.button = QPushButton(self)
        # 设置button控件文本
        self.button.setText('弹出对话框')
        # 移动button的位置
        self.button.move(50,50)

        # 将单击信号和槽绑定
        self.button.clicked.connect(self.showDialog)


    # 槽方法
    def showDialog(self):
        # 创建对话框
        dialog = QDialog()
        # 在对话框dialog里面放一个button
        button = QPushButton('确定',dialog)
        # 点击button按钮关闭  现成的槽
        button.clicked.connect(dialog.close)
        # 移动button
        button.move(50,50)
        # 给dialog设置标题
        dialog.setWindowTitle('对话框')
        # 设置对话框为模式状态，模式状态：即模式状态开启时，对话框窗口里的所有控件不可用
        dialog.setWindowModality(Qt.ApplicationModal)

        # 显示对话框
        dialog.exec()

# 防止别的脚本调用，只有自己单独运行时，才会调用下面的代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app = QApplication(sys.argv)
    # 创建对象
    main = QDialogDemo()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放)
    sys.exit(app.exec_())
