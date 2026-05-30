import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import os
from matplotlib.font_manager import FontProperties

current_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(current_dir, 'predict_result.mdb')
# 连接数据库
conn_str = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + str(db_file_path)
conn = pyodbc.connect(conn_str)

# 查询每一种类别的行数
categories = ['锈斑', '多余物', '焊接缺陷', '氧化物', '起皮', '鼓波', '划伤', '凹坑']
category_counts = []

for category in categories:
    query = f"SELECT COUNT(*) FROM result WHERE 检测结果 LIKE '%{category}%'"
    count = pd.read_sql_query(query, conn).iloc[0, 0]
    category_counts.append(count)


# 关闭数据库连接
conn.close()
# 过滤掉没有出现的类别
valid_categories = [category for category, count in zip(categories, category_counts) if count > 0]

valid_counts = [count for count in category_counts if count > 0]

# 创建颜色映射以便将每个类别与特定颜色关联
colors = plt.cm.Set3.colors
print(valid_counts)


# 设置中文显示
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)  # 替换为你系统中的中文字体路径
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 绘制扇形图
fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(valid_counts, labels=valid_categories, autopct='%1.1f%%', startangle=90, colors=colors)


# 在每个扇形上方添加标签和行数信息
for i, (category, count) in enumerate(zip(valid_categories, valid_counts)):
    radius = 1.2  # 控制标签离圆心的距离
    x = radius * plt.rcParams['font.size'] * 0.5 * (wedges[i].theta2 + wedges[i].theta1) * (3.14 / 180)
    y = radius * plt.rcParams['font.size'] * 0.5 * (wedges[i].theta2 + wedges[i].theta1) * (3.14 / 180)
    # ax.text(x, y, f'{count}', ha='center', va='center', fontsize=8, color='black')


# 添加图例

legend_labels = [f'{category}: {count}' for category, count in zip(valid_categories, valid_counts)]
ax.legend(wedges, legend_labels, title='检测结果', bbox_to_anchor=(1, 1))


plt.title('检测结果分布')
plt.savefig('./Type_distribution.png',bbox_inches='tight')
# plt.show()