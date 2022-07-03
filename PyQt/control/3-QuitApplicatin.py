# 退出应用程序
# 用到了水平布局，引入QHBoxLayout
# 需要一个控件，引入了QWidget
# 需要butoon，引入了QPushButton
import sys
from PyQt5.QtWidgets import QHBoxLayout,QMainWindow,QApplication,QPushButton,QWidget
# 用来添加图标
from PyQt5.QtGui import QIcon


class QuitApplication(QMainWindow):

    # 初始化
    def __init__(self):
        super(QuitApplication,self).__init__()

        # 设计窗口的尺寸
        self.resize(300,120)
        # 设置主窗口的标题
        self.setWindowTitle('退出应用程序')


        # 添加Button
        # 创建全局对象self.button1
        self.button1 = QPushButton('退出应用程序')

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


    # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)

    # 设置图标
    app.setWindowIcon(QIcon('images/001.jpg'))

    # 创建对象
    main = QuitApplication()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
