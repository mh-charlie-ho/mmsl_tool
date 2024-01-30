#!/usr/bin/env python

import rospy
from itri_msgs.msg import GroundFilterColData 


class RosNode:

    def __init__(self, nodeName):
        rospy.init_node(str(nodeName), anonymous=False)

    def Receiver(self, topicName, msgType):
        if not (len(topicName) == len(msgType)):
            print("check the argument quantity")
            return

        data = []
        amount = len(topicName)
        for i in range(amount):
            data.append(rospy.wait_for_message(str(topicName[i]), msgType[i]))

        return data


if __name__ == '__main__':
    rosNode = RosNode("ComeHere")
    data = rosNode.Receiver(["/col_pts", "/col_floating_obs_pts"], 
                            [GroundFilterColData, GroundFilterColData])
    print(data) # list
    print(data[0])
    print(type(data[0]))
