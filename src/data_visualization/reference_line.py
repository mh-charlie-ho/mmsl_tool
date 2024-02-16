#!/usr/bin/env python
import threading
import signal
import sys

import math
import time
import rospy

from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import std_msgs.msg
import tf

import numpy as np


def Monitor(source_frame, target_frame):
        listener = tf.TransformListener()
        trans = None
        rot = None
        ttime = None
        while not trans and not ttime:
            try:
                trans, rot = listener.lookupTransform(source_frame, target_frame, rospy.Time(0))
                ttime = listener.getLatestCommonTime(source_frame, target_frame)
                
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

        return (trans, rot, ttime)


def generate_points(angle, length=20.5):
    angle = angle/180*math.pi
    xrange = length*math.cos(angle)
    xdata = []
    ydata = []
    zdata = []
    
    '''
    When the x is zero, meaning the angel is 90 or -90,
    the xrange will be equal to zero. This function will be faulty.
    '''
    for x in np.arange(0.0, xrange, 0.01):
        for z in np.arange(0, 1, 0.05):
            v = (x, x*math.tan(angle), z)

            xdata.append(v[0])
            ydata.append(v[1])
            zdata.append(v[2])
    return xdata, ydata, zdata

def publish_point_cloud():
    rospy.init_node('reference_line', anonymous=True)

    pub = rospy.Publisher('/reference_line', PointCloud2, queue_size=10)
    rate = rospy.Rate(10)  # 1 Hz

    angle = rospy.get_param('/reference_line' + "/angle", default=41.5)
    length = rospy.get_param('/reference_line' + "/length", default=20.5)
    frame = rospy.get_param('/reference_line' + "/frameName", default="map")

    _,_,ttime = Monitor("map", frame)

    xdata, ydata, zdata = generate_points(angle, length)

    # Create a simple point cloud
    points = np.array([xdata, ydata, zdata]).T
    # Define the header for the PointCloud2 message
    while not rospy.is_shutdown():
        header = std_msgs.msg.Header()
        header.stamp = ttime # No helping because the latency of the tf update time is noticeable.
        
        header.frame_id = str(frame)

        # Create PointCloud2 message
        pc2_msg = pc2.create_cloud_xyz32(header, points)
    
        # Publish the PointCloud2 message
        pub.publish(pc2_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_point_cloud()

        
    except rospy.ROSInterruptException:
        pass

