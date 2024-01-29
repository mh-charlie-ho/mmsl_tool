import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# 创建图表
fig, ax = plt.subplots()
plt.xlim(0, 10)  # 设置 x 轴范围
plt.ylim(0, 10)  # 设置 y 轴范围

# 初始化点的坐标
x_values, y_values = [], []

# 绘制散点图
scatter = ax.scatter([], [], c='blue')  # 'blue' 表示蓝色

# 更新函数，用于每一帧更新散点位置
def update(frame):
    # 在示例中，我们将散点在 x 和 y 方向上每一帧都向右上方移动
    x = frame * 0.1
    y = frame * 0.1
    
    # 保存点的坐标
    x_values.append(x)
    y_values.append(y)
    
    # 更新散点位置
    scatter.set_offsets(np.column_stack((x_values, y_values)))

    return scatter,

# 创建动画
animation = FuncAnimation(fig, update, frames=range(100), interval=100)

# 显示动画
plt.show()
