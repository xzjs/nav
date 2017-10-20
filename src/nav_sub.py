#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''订阅服务器发送的消息并下发小车'''

import json
import math

import rospy
import zmq
from geometry_msgs.msg import PoseStamped
from nav_msgs.srv import GetPlan

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://172.18.29.153:5556")
socket.setsockopt(zmq.SUBSCRIBE, '')
rospy.init_node('send_client', anonymous=True)


def send(position):
    '''send goal'''
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    goal = PoseStamped()

    if position.has_key('action'):  # 判断是执行动作还是导航
        action = position['action']
        goal.header.frame_id = "base_link"
        if action == 'forward':
            goal.pose.position.x = 1
            goal.pose.orientation.w = 1
        if action == 'backward':
            goal.pose.position.x = -1
            goal.pose.orientation.w = 1
        if action == 'turnleft':
            goal.pose.orientation.w = math.sqrt(2) / 2
            goal.pose.orientation.z = math.sqrt(2) / 2
        if action == 'turnright':
            goal.pose.orientation.w = math.sqrt(2) / 2
            goal.pose.orientation.z = -math.sqrt(2) / 2
    else:
        goal.header.frame_id = "map"
        goal.pose.position.x = (int(position['x']) - 500) * 1.0 / 20
        goal.pose.position.y = -(int(position['y']) - 500) * 1.0 / 20
        goal.pose.position.z = 0.0
        goal.pose.orientation.x = 0.0
        goal.pose.orientation.y = 0.0
        goal.pose.orientation.z = 0.0
        goal.pose.orientation.w = 1.0
    rospy.loginfo(goal)
    rospy.sleep(1)
    pub.publish(goal)
    # get_plan()


def get_position():
    '''接受下发的指令'''
    while not rospy.is_shutdown():
        message = socket.recv()
        rospy.loginfo(message)
        send(json.loads(message))


def get_plan():
    '''获取导航路径'''
    rospy.wait_for_service('/move_base_node/make_plan')
    try:
        move_plan = rospy.ServiceProxy('/move_base_node/make_plan', GetPlan)
        resp = move_plan()
        rospy.loginfo(resp)
        return resp
    except rospy.ServiceException, e:
        rospy.logerr("Service call failed: %s" % e)


if __name__ == '__main__':
    try:
        get_position()
        # send(dict(action='turnright'))
    except rospy.ROSInterruptException:
        pass
