import datetime
import os
import sys

# 获取当前时间
current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
# 生成文件夹名称
# folder_name = current_time + sys.argv[1] + "模型和loss存放文件夹"
folder_name = current_time + sys.argv[1]
# 构建完整的路径
save_dir = os.path.join('logs', folder_name)
# 确保文件夹存在，如果不存在就创建
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
print(save_dir)