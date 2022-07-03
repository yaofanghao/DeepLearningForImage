# 让主窗口居中显示

# 通过QDesktopWidget类相应的API可以得到整个屏幕的尺寸
# 通过move方法移动窗口
import sys

# 从PyQt里面创建窗口和应用
from PyQt5.QtWidgets import QDesktopWidget,QMainWindow,QApplication
# 用来添加图标
from PyQt5.QtGui import QIcon

# 定义一个类，这个类从QMainWindow里面继承

class CenterForm(QMainWindow):

    # 初始化
    def __init__(self,parent=None):
        super(CenterForm,self).__init__(parent)

        # 设置主窗口的标题
        self.setWindowTitle('让窗口居中')

        # 设置窗口的尺寸
        self.resize(400,300)

        # 添加center方法，作用就是让窗口居中
        def center(self):
            # 创建实例，获得屏幕对象,得到屏幕的坐标系
            screen = QDesktopWidget().screenGeometry()

            # 得到窗口的坐标系
            size = self.geometry()

            # 获取屏幕的宽度、高度
            # 窗口左边缘的坐标等于(屏幕的宽度-窗口的宽度)/2
            newLeft = (screen.width()-size.width()) / 2

            # 屏幕上边缘的坐标等于(屏幕的高度-窗口的高度) / 2
            newTop = (screen.height() - size.height()) / 2

            # 移动窗口
            self.move(newLeft,newTop)

        #  获得状态栏
        # self.status = self.statusBar()
        #
        # # 在状态栏上，设置消息的状态时间5000ms
        # self.status.showMessage('只存在5秒的消息',5000)

    # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)

    # 设置图标
    # app.setWindowIcon(QIcon('images/001.jpg'))

    # 创建对象
    main =CenterForm()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())