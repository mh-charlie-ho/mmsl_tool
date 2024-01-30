#!/usr/bin/env python

import ros_node
from organize_msg import ManageMsg

import sys
import signal
import math
import numpy as np


def signal_handler(sig, frame):
    print("Ctrl+C pressed. Stopping animation.")
    sys.exit(0)


def AnalyzedData(xs, ys, rowLimit=None):
    '''
    xs = [0,1,2,0,8]
    ys = [0,1,2,0,7]
    '''
    if rowLimit is None:
        l = len(xs)
    elif rowLimit > len(xs):
        l = len(xs)
    else:
        l = rowLimit

    flag = 0
    for i in range(l):
        if xs[i]==0 or ys[i]==0:
            continue
        
        if flag==1:
            diffX = xs[i] - oldX
            diffY = ys[i] - oldY

            if math.atan(diffY/diffX) > math.pi/3:
                return True

        oldX = xs[i]
        oldY = ys[i]
        flag = 1

    return False


def Work(topicName, typeName, nodeName="node_name"):
    signal.signal(signal.SIGINT, signal_handler)

    node = ros_node.RosNode(nodeName)

    msgData = node.Receiver(topicName, typeName)[0]

    colStates = []
    for i, colData in enumerate(msgData.coldata):
        obj = ManageMsg({
            "rowid": list(colData.rowid),
            "range": list(colData.range),
            "height": list(colData.height),
            "type": list(colData.type),
            "intensity": list(colData.intensity)
        })
        xList = obj.GetCol(obj.GetRowData(), 'x').values
        yList = obj.GetCol(obj.GetRowData(), 'y').values
        colStates.append(AnalyzedData(xList, yList, rowLimit=20))
    
    print(np.where(colStates==True)[0])

