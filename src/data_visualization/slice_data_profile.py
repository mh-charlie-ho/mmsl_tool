#!/usr/bin/env python

import ros_node
import general_test_data
from organize_msg import ManageMsg

from itri_msgs.msg import GroundFilterColData

import sys
import signal
import threading
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation


class UpdateContainer():
    def __init__(self):
        self.mX = []
        self.mY = []

        self.mLocker = threading.Lock()
    def append(self, x, y):
        with self.mLocker:
            self.mX.append(x)
            self.mY.append(y)

    def clear(self):
        with self.mLocker:
            self.mX.clear()
            self.mY.clear()

    def print_data(self):
        print((self.mX, self.mY))


def signal_handler(sig, frame):
    print("Ctrl+C pressed. Stopping animation.")
    sys.exit(0)


def Update(msgObj, dataObj, rowid):
    x = msgObj.GetCol(msgObj.GetRowData(rowId=rowid, index=0), "x")
    y = msgObj.GetCol(msgObj.GetRowData(rowId=rowid, index=0), "y")
    print(x,y)
    dataObj.append(x, y)
    return (dataObj.mX, dataObj.mY)


def PlotUpdate(frame):
    print("=========================frame: ", frame)
    for i in range(axesNum):
        print("here")
        x, y = Update(structMsgData[i], dataCon[i], rowid=frame)
        scatter[i].set_offsets(np.column_stack((x, y)))
    
    return scatter,

def PrintDict(dict):
    for i in dict:
        print(i, dict[i])

def Work(topicName, typeName, color, nodeName="node_name"):
    global axesNum, scatter, structMsgData, dataCon
    signal.signal(signal.SIGINT, signal_handler)

    node = ros_node.RosNode(nodeName)

    dataList = node.Receiver(topicName, typeName)
    axesNum = len(dataList)

    # organize msg
    for i in range(axesNum):
        data = dataList[i]
        dataList[i] = {
            "rowid": list(data.rowid),
            "range": list(data.range),
            "height": list(data.height),
            "type": list(data.type),
            "intensity": list(data.intensity)
        }
    
    # For Test =================================================================
    # dataList = []
    # for i in range(3):
    #     generator = general_test_data.Generator()
    #     generator.Do(100)
    #     dataList.append(generator.GetDict())

    # axesNum = len(dataList)
    
    # for i in range(axesNum):
    #     PrintDict(dataList[i])
    #     print(" ")
    # ==========================================================================
    # plot
    fig, ax = plt.subplots()
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_xlim(left=-20, right=120)
    ax.set_ylim(bottom=-20, top=120)
    ax.set_title("TEST")
    ax.grid(True, linestyle='--', linewidth=0.5)

    structMsgData = []
    dataCon = []
    scatter = []
    for i in range(axesNum):
        structMsgData.append(ManageMsg(dataList[i]))
        dataCon.append(UpdateContainer())
        scatter.append(ax.scatter([], [], c=color[i]))
    
    
    if len(structMsgData)==0 or len(structMsgData)==0:
        sys.exit()

    animation = FuncAnimation(fig, PlotUpdate, frames=range(100), interval=1000)
    plt.show()  
    

if __name__ == '__main__':
    # For Test =================================================================
    topicName = ["/col_pts", "/col_floating_obs_pts"]
    typeName = [GroundFilterColData, GroundFilterColData]
    color = ['b','g']
    # ==========================================================================
    Work(topicName, typeName, color)

    
