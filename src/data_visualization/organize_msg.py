#!/usr/bin/env python

import pandas as pd
from data_points import DataPoints


class ManageMsg(DataPoints):

    def __init__(self, msgData, rowEndId=None):
        super(ManageMsg, self).__init__(
            msgData["range"],
            msgData["height"],
            msgData["rowid"],
            msgData["type"],
        )

        self.__SetOrderFrame(rowEndId) # self.__mOrderFrame
    
    def __SetOrderFrame(self, rowEndId):
        dataFrame = pd.DataFrame({
            'rowid': self.mRowIds,
            'x': self.mXs,
            'y': self.mYs,
            'type': self.mTypes
        })

        existingRowid = dataFrame['rowid'].values
        # print("how many?: ", len(existingRowid))

        if rowEndId is None:
            if len(existingRowid)==0:
                rowEndId = 0
            else:
                rowEndId = max(existingRowid)

        missingRows = set(range(rowEndId)) - set(existingRowid)

        subDataFrame = pd.DataFrame({
            'rowid': list(missingRows),
            'x': 0, 
            'y': 0, 
            'type': 0
        })

        newDataFrame = pd.concat([dataFrame, subDataFrame], ignore_index=True)
        self.__mOrderFrame = newDataFrame.sort_values(
            ['rowid', 'x'], ascending=True).reset_index(drop=True)
    
    def GetRowData(self, rowId=None, index=None):

        if rowId is None or len(self.__mOrderFrame)==0:
            return self.__mOrderFrame
        
        if rowId not in self.__mOrderFrame['rowid'].values:
            return self.__mOrderFrame.loc[len(self.__mOrderFrame)-1]
        
        dataFrame = (self.__mOrderFrame[
            self.__mOrderFrame['rowid']==rowId]).reset_index(drop=True)   
           
        if index is None:
            return dataFrame
        
        index = index \
            if index <= len(dataFrame) else len(dataFrame)-1
        if index == -1:
            index = len(dataFrame)-1
        
        return dataFrame.loc[index]
    
    def GetCol(self, formatData, colnumName):
        '''
        TBD
        Check the col name is existing. 
        '''
        return formatData[str(colnumName)].tolist()

if __name__ == '__main__':
    # testDict = {
    #     "rowid":  [0, 0, 0, 0, 0, 0, 0, 0],
    #     "type":   [  0,   0,   0,   0,   0,   0,   0,   0],
    #     "range":  [ 0.000000, 1.766293, 2.445991, 3.195587, 3.602719, 3.911899,
    #                 4.134902, 4.402998],
    #     "height": [ 0.000000, 26.402569, 86.429100, 26.110262, 26.780521,
    #                27.411665, 35.315552, 27.092993]
    # }

    testDict = {
        "rowid": [],
        "type" : [],
        "range"    : [],
        "height"    : []
    }

    testObj = ManageMsg(testDict)
    print(testObj.GetCol(testObj.GetRowData(), "x"))
    print(" ")
    # print(testObj.GetRowData(rowId=2))
    # pandas = testObj.GetRowData(rowId=2)
    # print(testObj.GetCol(pandas, "x"))
    # print(" ")
    # print(testObj.GetRowData(rowId=2, index=3))

    # series = testObj.GetRowData(rowId=2, index=3)
    # print(testObj.GetCol(series, "x"))


    #    rowid  type         x          y
    # 0    0.0     0  0.000000   0.000000
    # 1    0.0     0  1.766293  26.402569
    # 2    0.0     0  2.445991  86.429100
    # 3    0.0     0  3.195587  26.110262
    # 4    0.0     0  3.602719  26.780521
    # 5    0.0     0  3.911899  27.411665
    # 6    0.0     0  4.134902  35.315552
    # 7    0.0     0  4.402998  27.092993

    table = pd.DataFrame({
        "rowid": [],
        "type" : [],
        "x"    : [],
        "y"    : []
    })
