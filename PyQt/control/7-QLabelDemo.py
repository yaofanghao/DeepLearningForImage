# QLabel控件的基本用法

import sys
# 导入QLabel模块  QVBoxLayout垂直布局  (QHBoxLayout 水平布局)
from PyQt5.QtWidgets import QVBoxLayout,QMainWindow,QApplication,QLabel,QWidget
# 导入调制板，调制QLabel背景色
# 导入显示图片包QPixmap
from PyQt5.QtGui import QPixmap,QPalette
# 导入一些Qt的常量
from PyQt5.QtCore import Qt

# 编写一个类，从QWidget中继承
class QLabelDemo(QWidget):
    def __init__(self):
        super().__init__()
        # 调用初始化UI的一个方法
        self.initUI()

    # 规范代码，初始化UI直接写在一个方法里
    def initUI(self):
        # 创建四个label控件
        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        label4 = QLabel(self)


        # 给label1设置文本,支持html的标签
        label1.setText("<font color=purpel>这是一个文本标签.</font>")
        # 用调试板自动填充背景
        label1.setAutoFillBackground(True)
        # 创建调试板
        palette = QPalette()
        # 给调试板设置背景色
        palette.setColor(QPalette.Window,Qt.blue)
        # 对label1使用调试板
        label1.setPalette(palette)
        # 让label1居中对齐
        label1.setAlignment(Qt.AlignCenter)


        # 给label2设置<a>标签
        label2.setText("<a href='#'>欢迎使用Python GUI程序</a>")  # 可以在a标签里触发事件或者跳转网页 二者选其一

        # 给label3设置文本居中
        label3.setAlignment(Qt.AlignCenter)
        # 给label3设置提示文本
        label3.setToolTip('这是一个图片标签')
        # 让label3显示图片
        label3.setPixmap(QPixmap("./images/001.jpg"))   # 同级目录写法./images

        # 给label4设置文本内容
        label4.setText("<a href='https://www.baidu.com/'>打开百度</a>")  # setText里面的内容要用双引号，单引号会报错
        # 让label4打开链接
        # 如果设为True,用浏览器打开网页，如果设为False,调用槽函数
        label4.setOpenExternalLinks(True)
        # 让label4的文本右对齐
        label4.setAlignment(Qt.AlignRight)
        # 给label4设置提示文本
        label4.setToolTip('这是一个超链接')

        # 创建一个垂直布局
        vbox = QVBoxLayout()
        # 分别把这四个控件放到这个布局里面           布局函数 addWidget
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)

        # 将信号与槽绑定
        label2.linkHovered.connect(self.linkHovered)
        label4.linkActivated.connect(self.linkClicked)

        # 设置布局
        self.setLayout(vbox)
        self.setWindowTitle('QLabel控件演示')
        # 设置标题


    # 槽有两个方法 1.滑过  2.单击
    def linkHovered(self):
        print("当鼠标滑过label2标签时，触发事件")

    def linkClicked(self):
        print("当鼠标单击label4标签时，触发事件")

  # 防止别的脚本调用，只有自己单独运行，才会调用下面代码
if __name__ == '__main__':

    # 创建app实例，并传入参数
    app =  QApplication(sys.argv)

    # 设置图标
    # app.setWindowIcon(QIcon('images/001.jpg'))

    # 创建对象
    main = QLabelDemo()

    # 创建窗口
    main.show()

    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
