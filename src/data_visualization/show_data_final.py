import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading


class DataPoint(object):

    def __init__(self):
        self.mX = 0
        self.mY = 0
        self.mRowId = 0
        self.mType = 0


class DataPoints(DataPoint):

    def __init__(self):
        super(DataPoints,self).__init__()
        self.mXs = []
        self.mYs = []
        self.mRowIds = []
        self.mTypes = []


class AnimationAxesData:
    
    def __init__(self, ax, msgData, pointColor, rowEndNum=None):
        self.ax = ax
        self.msgData = msgData

        self.mDataPoints = DataPoints()
        self.__scatterObj = self.ax.scatter([], [], c=str(pointColor))

        self.__SetDataFrame(rowEndNum)

        self.mX = []
        self.mY = []

        self.mLocker = threading.Lock()

    def GetRawData(self, index):
        self.mDataPoints.mRowId = self.msgData.rowid[index]
        self.mDataPoints.mX = self.msgData.range[index]
        self.mDataPoints.mY = self.msgData.height[index]
        self.mDataPoints.mType = self.msgData.type[index]
        return self.mDataPoints

    def __SetDataFrame(self, rowEndNum=None):
        dataFrame = pd.DataFrame({
            'rowid': self.msgData.rowid,
            'x': self.msgData.range,
            'y': self.msgData.height,
            'type': self.msgData.type
        })

        existingRowid = dataFrame['rowid'].values

        if rowEndNum is None:
            rowEndNum = max(existingRowid)

        missingRows = set(range(rowEndNum)) - set(existingRowid)

        subDataFrame = pd.DataFrame({
            'rowid': list(missingRows),
            'x': 0, 
            'y': 0, 
            'type': 0
        })

        newDataFrame = pd.concat([dataFrame, subDataFrame], ignore_index=True)
        self.__mDataFrame = newDataFrame.sort_values(
            ['rowid', 'x'], ascending=True).reset_index(drop=True)

    def GetDataFrame(self):
        return self.__mDataFrame
    
    def GetRowData(self, rosId=0, number=1):
        subDataFrame = (
            self.__mDataFrame[self.__mDataFrame['rowid']==rosId])[0:number]
        dataPoints = [
            subDataFrame['rowid'].values,
            subDataFrame['x'].values,
            subDataFrame['y'].values,
            subDataFrame['type'].values]
        return dataPoints

    def UpdateData(self, rowid, number=1):
        with self.mLocker:
            dataPoints = self.GetRowData(rowid, number)
            self.mX.extend(dataPoints[1])
            self.mY.extend(dataPoints[2])

            self.__scatterObj.set_offsets(np.column_stack((self.mX, self.mY)))
        
    def GetAxesObj(self):
        with self.mLocker:
            return self.__scatterObj

    def ClearData(self):
        with self.mLocker:
            self.mX.clear()
            self.mY.clear()

    def Show(self, fig=None, frames=100, threading=None):
        if fig is None:
            fig, ax = plt.subplots()

        FuncAnimation(fig, self.UpdateData, frames=range(frames), interval=100)
        plt.show()