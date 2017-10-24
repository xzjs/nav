#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''scan ROS Node'''
import time

# license removed for brevity
import rospy
import zmq
from sensor_msgs.msg import LaserScan

import requests
import random

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://172.18.29.153:5555")
# socket.connect("tcp://127.0.0.1:5555")
i = 0


def callback(data):
    '''scan Callback Function'''
    # rospy.loginfo(len(data.ranges))
    global i
    pic = requests.get(
        'http://192.168.12.20/img/laser_map/laser_map_' + str(i) + '.png?' + str(time.time()))
    socket.send(pic.content + "---scan")
    response = socket.recv()
    print "laser", response
    if i == 19:
        i = 0
    else:
        i = i + 1


def listener():
    '''scan Subscriber'''

    rospy.Subscriber("/f_scan", LaserScan, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def talker():
    '''scan Publisher'''
    rospy.init_node('my_scan', anonymous=True)
    listener()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
