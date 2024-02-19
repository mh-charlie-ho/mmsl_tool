#!/usr/bin/env python
import signal, sys
import ros_node

from itri_msgs.msg import GroundFilterColDataList
from organize_msg import ManageMsg

from slice_data_profile import UpdateContainer as upc

import numpy as np
import matplotlib.pyplot as plt



def signal_handler(sig, frame):
    print("Ctrl+C pressed. Stopping animation.")
    sys.exit(0)

def GenerateLine():
    '''
    TBD
    parameterize 83 degree in launch file
    '''
    angle = np.radians(83)
    dafaultPoint = [500, 0]

    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])

    return np.dot(rotation_matrix, np.array(dafaultPoint)).tolist()

def Work(topicName, typeName, nodeName="node_name"):
    node = ros_node.RosNode(nodeName)
    msgData = node.Receiver(topicName, typeName)[0]

    dataSet = []
    for i, colData in enumerate(msgData.coldata):
        obj = ManageMsg({
            "rowid": list(colData.rowid),
            "range": list(colData.range),
            "height": list(colData.height),
            "type": list(colData.type),
            "intensity": list(colData.intensity)
        })
        List = np.array(obj.GetCol(obj.GetRowData(), 'x'))
        rangeList = np.array(List)

        
        container = upc()
        print(i*0.175)
        x = (rangeList* np.cos(i*0.175/180*3.1415926)).tolist()
        y = (rangeList* np.sin(i*0.175/180*3.1415926)).tolist()
        
        
        container.append(x, y)
        dataSet.append(container)

    return dataSet

def DataArrangement(dataSet):
    xList = []
    yList = []
    for data in dataSet:
        xList.extend(data.mX)
        yList.extend(data.mY)

    return xList,yList 


def Plot(x, y):
    plt.figure("TOP-DOWN")
    plt.axis('square')

    line = GenerateLine()
    
    plt.plot([0,line[0]], [0, line[1]])
    plt.scatter(x, y, color='blue', marker='o', s=2)

    plt.title('Scatter Plot Example')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.xlim(-50,50)
    plt.ylim(-50,50)
    plt.grid()

    print("show")

    signal.signal(signal.SIGINT, signal_handler)
    plt.show()


if __name__ == '__main__':
    # For Test =================================================================
    topicName = ["/all_points",]
    typeName = [GroundFilterColDataList]
    # ==========================================================================
    dataSet = Work(topicName, typeName)
    x, y = DataArrangement(dataSet)
    Plot(x, y)