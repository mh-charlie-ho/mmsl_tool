import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

from typing import List

fig, ax = plt.subplots()
x_data = np.linspace(0, 2 * np.pi, 100)
line, = ax.plot(x_data, np.sin(x_data))


def update(frame):
    y_data = np.sin(x_data + frame * 0.1)
    line.set_ydata(y_data)
    return line,


animation = FuncAnimation(fig, update, frames=range(100), interval=50)

plt.show()


class DataPoint:

    def __init__(self) -> None:
        self.mX = 0
        self.mY = 0
        self.mRowId = 0
        self.mType = 0


class DataPoints(DataPoint):

    def __init__(self) -> None:
        super().__init__()
        self.mXs = []
        self.mYs = []
        self.mRowIds = []
        self.mTypes = []



class AnimationAxesData:
    def __init__(self, ax, msgData, pointColor, pointsymbol) -> None:
        self.ax = ax
        self.msgData = msgData

        self.mDataPoints = DataPoints()
        self.__scatterObj = self.ax.scatter([], [], c=str(pointColor))

    def GetData(self, index):
        self.mDataPoints.mRowId = self.msgData.rowId[index]
        self.mDataPoints.mX = self.msgData.range[index]
        self.mDataPoints.mY = self.msgData.height[index]
        self.mDataPoints.mType = self.msgData.type[index]
        return self.mDataPoints

    def GetAxesObj(self, xValues:List[float]=[0.0], yValues:List[float]=[0.0]):
        self.__scatterObj.set_offsets(np.column_stack((xValues, yValues)))
        return self.__scatterObj

    def __SetDataFrame(self):
        dataFrame = pd.DataFrame({
            'rowid': self.msgData.rowId,
            'x': self.msgData.range,
            'y': self.msgData.height,
            'type': self.msgData.type
        })

        self.mDataFrame = dataFrame.sort_values(['rowid'],ascending=True)




    def UpdateAxes(self, index, *, method='scatter'):
        if method not in self.__GetSupportMethod():
            print("No support ths method!")
            return
        
        dataPoints = self.GetData(index)
        
        





class Animation:

    def __init__(self, dataList: List, plotColor: List) -> None:
        fig, self.ax = plt.subplots()

        if ~(len(dataList) == len(plotColor)):
            print('check the argument quantity')
            return

        self.mDataList = dataList
        self.mColor = plotColor

        self.mContainer = []
        self.mScatter = []

        self.mLocker = threading.Lock()

        self.__SetDataContainer()
        self.__SetScatter()

    def __SetDataContainer(self) -> None:
        for i in self.mDataList:
            self.mContainer.append(DataPoints())

    def __SetScatter(self):
        for i in self.mColor:
            self.mScatter = [].append(self.ax.scatter([], [], c=str(i)))

    def UpdateData(self, frame):
        with self.mLocker:
            for id, datalist in enumerate(self.mDataList):
                data = self.mContainer[id]
                # Here should be match the ros msg type
                data.mRowIds.append(datalist.RowId[frame])
                data.mXs.append(datalist.range[frame])
                data.mYs.append(datalist.height[frame])
                data.mTypes.append(datalist.type[frame])

    def UpdatePlot(self):


    scatter.set_offsets(np.column_stack(()))

    x_data = np.linspace(0, 2 * np.pi, 100)
    line, = ax.plot(x_data, np.sin(x_data))
