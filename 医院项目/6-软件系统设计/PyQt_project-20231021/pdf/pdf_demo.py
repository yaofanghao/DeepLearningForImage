from reportlab.pdfbase import pdfmetrics  # 注册字体
from reportlab.pdfbase.ttfonts import TTFont  # 字体类
from reportlab.pdfgen import canvas  # 创建pdf文件

# from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, Image  # 报告内容相关类
# from reportlab.lib.pagesizes import letter  # 页面的标志尺寸(8.5*inch, 11*inch)
# from reportlab.lib.styles import getSampleStyleSheet  # 文本样式
# from reportlab.lib import colors  # 颜色模块
# from reportlab.graphics.charts.barcharts import VerticalBarChart  # 图表类
# from reportlab.graphics.charts.legends import Legend  # 图例类
# from reportlab.graphics.shapes import Drawing  # 绘图工具
# from reportlab.lib.units import cm  # 单位：cm

# 1 注册字体(提前准备好字体文件, 如果同一个文件需要多种字体可以注册多个)

# TTFomt(字体名,字体文件路劲)
pdfmetrics.registerFont(TTFont('yang', 'C:/Users/Lenovo/Desktop/上海医学qtGUI/生成word测试/yangziti.ttf'))

# 2.创建空白pdf文件
pdf_file = canvas.Canvas("C:/Users/Lenovo/Desktop/上海医学qtGUI/生成word测试/kongbai.pdf")

# 3.写字体
# 设置字体
pdf_file.setFont("yang", 40)
# 设置文字颜色
# r g b 范围（0（0）-1（255） ）  最后透明度

pdf_file.setFillColorRGB(1, 0, 0, 1)

# 渲染文字
pdf_file.drawString(100, 100, "yang")

# 保存
pdf_file.save()
