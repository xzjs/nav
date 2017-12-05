#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''scan ROS Node'''
import json
import time

# license removed for brevity
import rospy
import zmq
from sensor_msgs.msg import LaserScan


# socket.connect("tcp://127.0.0.1:5555")


def callback(data):
    '''scan Callback Function'''
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://172.18.29.153:5559")
    print data
    d = {'frame_id': data.header.frame_id, 'ranges': data.ranges}

    socket.send_json(d)
    response = socket.recv()
    print "laser", response


def listener():
    '''scan Subscriber'''

    rospy.Subscriber("/scan", LaserScan, callback)

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
