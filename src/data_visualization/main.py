#!/usr/bin/env python
import ros_node
import show_data_final as sdf
from itri_msgs.msg import GroundFilterColData

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import sys


def Update(frame, axList):
    print(len(axList))

    tmp = []
    for ax in axList:
        print(ax.GetDataFrame())
        print(ax.GetRowData())
        input()
        ax.UpdateData(frame)
        print(ax.mX, ax.mY)
        tmp.append(ax.GetAxesObj())

    return tmp

if __name__ == '__main__':
    topicName = ["col_pts"]
    typeName = [GroundFilterColData]
    
    node = ros_node.RosNode("node_name")
    dataList = node.Receiver(topicName, typeName)
    
    axList = []
    pointColor = ['blue', 'red']
    
    print(dataList)

    fig, ax = plt.subplots()
    for i in range(len(dataList)):
        axList.append(sdf.AnimationAxesData(
            ax, dataList[i], pointColor[i]))  # rowEndNum=10
    
    print(len(axList))

    if len(axList) == 0:
        sys.exit()

    ani = FuncAnimation(fig, Update, fargs=(axList,), frames=range(100), interval=100)
    plt.show()


    
    
