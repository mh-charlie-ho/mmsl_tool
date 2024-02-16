from data_visualization.data_points import DataPoints
import inspect


def MemberList(obj):
    # list all member in the class
    return [
        var for var, _ in inspect.getmembers(obj) if not var.startswith('__')
    ]


obj = DataPoints([1, 2], [1, 2], [1, 2], [1, 2])
print(MemberList(obj))
print(obj.__dict__)
obj.Extract(1)
print(obj.__dict__)
