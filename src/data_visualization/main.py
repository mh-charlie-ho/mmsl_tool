import rosnode


if __name__ == '__main__':
    topicName = ["col_pts"]
    typeName = []

    node = rosnode.RosNode("node_name")
    dataList = node.Receiver(topicName, typeName)

    '''
    dataList[0] = 
    [
    rowid = []
    range = []
    height = []
    type = []
    #intnesity = []
    #coordinate = []
    ]
    '''

    
    
