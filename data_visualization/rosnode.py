#!/usr/bin/env python
import rospy
from typing import List


def print_():
    print("Apple")


class RosNode:

    def __init__(self, nodeName) -> None:
        rospy.init_node(str(nodeName), anonymous=True)

    def Receiver(self, topicName: List[str], msgType: List[str]) -> List:
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
    pass
