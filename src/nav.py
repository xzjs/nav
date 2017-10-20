#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''send goal'''

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import rospy
import roslib
roslib.load_manifest('slam')
import actionlib
from geometry_msgs.msg import PoseStamped


def send_goal():
    '''send'''

    rospy.init_node('send_goal_client')
    client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()
    goal = MoveBaseGoal()    
    goal.target_pose.header.frame_id = "base_link"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 1
    goal.target_pose.pose.position.y = 0
    goal.target_pose.pose.orientation.w = 1
    rospy.loginfo(goal)
    client.send_goal(goal)
    finished_within_time = client.wait_for_result(rospy.Duration(60))
    if not finished_within_time:
        client.cancel_goal()
        rospy.loginfo("Timed out achieving goal")
    else:
        state = client.get_state()
        rospy.loginfo(state)


if __name__ == '__main__':
    send_goal()
