# 显示控件的提示信息

# 需要用到 QToolTip

import sys
from PyQt5.QtWidgets import  QHBoxLayout,QMainWindow,QApplication,QToolTip,QPushButton,QWidget
# 提示信息需要设置字体
from PyQt5.QtGui import QFont



class TooltipForm(QMainWindow):
    def __init__(self):
        super().__init__()
        # 调用初始化ui的一个方法
        self.initUI()

    # 编写初始化UI的方法
    def initUI(self):
        # 设置字体和字号
        QToolTip.setFont(QFont('SansSerif',12))
        # 给窗口设置提示，这个方法支持富文本
        self.setToolTip('今天是个<b>好日子</b>')
        # 设置窗口的位置和尺寸
        self.setGeometry(300,300,200,200)
        # 设置窗口的标题
        self.setWindowTitle('设置控件提示消息')

    # 添加butoon按钮并设置提示信息

        # 添加Button
        # 创建全局对象self.button1
        self.button1 = QPushButton('我的按钮')
        # 设置按钮提示
        self.button1.setToolTip('这是按钮的提示信息')
        # 发送单击信号，执行对应的方法  (将信息与槽关联)
        self.button1.clicked.connect(self.onClick_Button)

        # 创建水平布局
        layout = QHBoxLayout()
        # 将组件加到水平局部里面
        layout.addWidget(self.button1)

        # 放置一个主框架
        mainFrame = QWidget()
        # 在主框架内添加水平布局
        mainFrame.setLayout(layout)
        # 把主框架放在窗口上
        self.setCentralWidget(mainFrame)

    # 按钮的单击事件的方法(自定义的槽)
    def onClick_Button(self):
        sender = self.sender()
        print(sender.text() + '按钮被按下')
        # 得到实例
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

# 防止别的脚本调用，只有自己单独运行时，才会调用下面代码
if __name__ == '__main__':
    # 创建app实例，并传入参数
    app= QApplication(sys.argv)
    # 创建对象
    main = TooltipForm()
    # 创建窗口
    main.show()
    # 进入程序的主循环，并通过exit函数，确保主循环安全结束(该释放资源的释放资源)
    sys.exit(app.exec_())


