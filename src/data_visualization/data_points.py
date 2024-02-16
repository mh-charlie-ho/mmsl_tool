#!/usr/bin/env python


class DataPoint(object):

    def __init__(self, x=0, y=0, rowid=0, type=0):
        self.mX = x
        self.mY = y
        self.mRowId = rowid
        self.mType = type


class DataPoints(DataPoint):

    def __init__(self, xs=[], ys=[], rowids=[], types=[]):
        super(DataPoints, self).__init__()
        self.mXs = xs
        self.mYs = ys
        self.mRowIds = rowids
        self.mTypes = types

    def Extract(self, id):
        super(DataPoints, self).__init__(self.mXs[id], self.mYs[id],
                                         self.mRowIds[id], self.mTypes[id])


if __name__ == '__main__':
    # test the class
    import inspect

    def MemberList(obj):
        # list all member in the class
        return [
            var for var, _ in inspect.getmembers(obj)
            if not var.startswith('__')
        ]

    obj = DataPoints([1, 2], [1, 2], [1, 2], [1, 2])
    print(MemberList(obj))
    print(obj.__dict__)
    obj.Extract(1)
    print(obj.__dict__)
