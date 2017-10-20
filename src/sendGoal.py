#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''send goal'''

import rospy
from geometry_msgs.msg import PoseStamped
import time


def send():
    '''send goal'''
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
    rospy.init_node('send111_client', anonymous=True)
    goal = PoseStamped()
    goal.header.frame_id = "map"
    goal.pose.position.x = 1.0
    goal.pose.position.y = 1.0
    goal.pose.position.z = 0.0
    goal.pose.orientation.x = 0.0
    goal.pose.orientation.y = 0.0
    goal.pose.orientation.z = 0.0
    goal.pose.orientation.w = 1.0
    rospy.loginfo(goal)
    rospy.sleep(1)
    pub.publish(goal)


if __name__ == '__main__':
    send()
