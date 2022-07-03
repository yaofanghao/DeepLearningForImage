# 第一个主窗口
# 把所有和UI有关的代码都放在一个类里面，创建窗口只要创建类的实例就可以了

import sys

# 从PyQt里面创建窗口和应用
from PyQt5.QtWidgets import QMainWindow,QApplication
# 用来添加图标
from PyQt5.QtGui import QIcon

# 定义一个类，这个类从QMainWindow里面继承

class FristMainWin(QMainWindow):

    # 初始化
    def __init__(self,parent=None):
        super(FristMainWin,self).__init__(parent)

        # 设置主窗口的标题
        self.setWindowTitle('第一个主窗口应用')

        # 设置窗口的尺寸
        self.resize(400,300)
        # 获得状态栏
        self.status = self.statusBar()

        # 在状态栏上，设置消息的状态时间5000ms
        self.status.showMessage('只存在5秒的消息',5000)

    # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)

    # 设置图标
    app.setWindowIcon(QIcon('images/001.jpg'))

    # 创建对象
    main = FristMainWin()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())


