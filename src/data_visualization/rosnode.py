#!/usr/bin/env python
import rospy

from itri_msgs.msg import GroundFilterColData 


def print_():
    print("Apple")


class RosNode:

    def __init__(self, nodeName):
        rospy.init_node(str(nodeName), anonymous=True)

    def Receiver(self, topicName, msgType):
        if ~(len(topicName) == len(msgType)):
            print("check the argument quantity")
            return

        data = []
        amount = len(topicName)
        for i in range(amount):
            data.append(
                rospy.wait_for_message(str(topicName[i]), len(msgType[i])))

        return data


if __name__ == '__main__':
    GroundFilterColData.rowid = 0.0
    print(GroundFilterColData.rowid)
