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


a  = DataPoints()

print(a.mX)