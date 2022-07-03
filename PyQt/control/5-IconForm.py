# 设置窗口和应用程序图标

# 窗口的setWindowIcon方法设置窗口的图标，只在Windows和linux中可用，mac不可用

import sys

# 从PyQt里面创建窗口和应用
from PyQt5.QtWidgets import QMainWindow,QApplication
# 用来添加图标
from PyQt5.QtGui import QIcon

# 定义一个类，这个类从QMainWindow里面继承

class IconForm(QMainWindow):

    # 初始化
    def __init__(self,parent=None):
        super(IconForm,self).__init__(parent)
        self.initUI()

    # 规范代码，初始化直接写在一个方法里
    def initUI(self):
        # 设置坐标系，可用同时设置窗口的尺寸和位置
        self.setGeometry(400,400,250,450)
        # 设置主窗口的标题
        self.setWindowTitle('设置窗口图标')
        # 设置窗口图标
        self.setWindowIcon(QIcon('./images/001.jpg'))
        # self.setWindowIcon(QIcon('/images/3.ico'))   这行代码失效，原因：图片路径表示问题
        # # 设置窗口的尺寸
        # self.resize(400,300)
        # 获得状态栏
        # self.status = self.statusBar()
        #
        # # 在状态栏上，设置消息的状态时间5000ms
        # self.status.showMessage('只存在5秒的消息',5000)

    # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)
    # QApplication中的setWindowIcon方法用于设置主窗口的图标和应用程序图标，但调用了窗口的setWinodowIcon方法
    # QApplication中的setWindowIcon方法就只能用于设置应用程序图标了
    # 设置图标
    # app.setWindowIcon(QIcon('images/horse.jpg'))

    # 创建对象
    main = IconForm()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())