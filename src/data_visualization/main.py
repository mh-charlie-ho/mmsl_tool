#!/usr/bin/env python
import slice_data_profile

from itri_msgs.msg import GroundFilterColData

if __name__ == '__main__':
    # For Test =================================================================
    topicName = ["/col_pts", "/col_floating_obs_pts"]
    typeName = [GroundFilterColData, GroundFilterColData]
    # ==========================================================================

    slice_data_profile.Work(topicName, typeName)