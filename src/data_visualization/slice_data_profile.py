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
        if not (type(x) == type(y)):
            raise "Appending different type data"
        
        if type(x) is list:
            with self.mLocker:
                self.mX.extend(x)
                self.mY.extend(y)
        else:
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


def Update(msgObj, dataObj, rowid, rowLen):
    rowid = msgObj.GetCol(msgObj.GetRowData(rowId=rowid, index=-1), "rowid")
    x = msgObj.GetCol(msgObj.GetRowData(rowId=rowid, index=-1), "x")
    y = msgObj.GetCol(msgObj.GetRowData(rowId=rowid, index=-1), "y")
    print(rowid, x, y)
    # print(msgObj.GetRowData())
    # print("=====")
    if len(dataObj.mX)<=rowLen:  # stop it in the max row
        dataObj.append(x, y)
    return (dataObj.mX, dataObj.mY)


def PlotUpdate(frame, frameNum):
    print("=========================frame: ", frame)
    for i in range(axesNum):
        print("here")
        x, y = Update(structMsgData[i], dataCon[i], rowid=frame, rowLen=frameNum)
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
    print("Received")
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
    ax.set_xlim(left=-5, right=100)
    ax.set_ylim(bottom=-5, top=30)
    ax.set_title("TEST")
    ax.grid(True, linestyle='--', linewidth=0.5)

    structMsgData = []
    dataCon = []
    scatter = []
    for i in range(axesNum):
        structMsgData.append(ManageMsg(dataList[i]))
        dataCon.append(UpdateContainer())
        scatter.append(ax.scatter([], [], c=color[i]))
    
    # sys.exit()
    
    if len(structMsgData)==0 or len(structMsgData)==0:
        sys.exit()

    frameNum = 300
    animation = FuncAnimation(
        fig, PlotUpdate, frames=range(frameNum), fargs=(frameNum,), interval=80)
    plt.show()  
    

if __name__ == '__main__':
    # For Test =================================================================
    topicName = [
                 "/col_ground_pts", 
                #  "/col_nonground_pts",
                 "/col_ground_obs_pts", 
                 "/col_floating_obs_pts"
                ]
    typeName = [
                GroundFilterColData,
                # GroundFilterColData, 
                GroundFilterColData, 
                GroundFilterColData
               ]
    color = [
             'y',
            #  'r',
             'r',
             'g'
            ]
    # ==========================================================================
    Work(topicName, typeName, color)

    
