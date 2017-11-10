#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''pointCloud ROS Node'''
import json

import rospy
import zmq
from sensor_msgs.msg import PointCloud2
import pcl
import pickle


def callback(data):
    '''pointCloud Callback Function'''
    byte_data = pickle.dumps(data)
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://172.18.29.153:5555")
    s = str(byte_data) + '---pointCloud'
    socket.send(s)
    response = socket.recv()
    print "point", response


def listener():
    '''pointCloud Subscriber'''
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('pointCloud', anonymous=True)

    rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
