#!/usr/bin/env python
'''pointCloud ROS Node'''
import rospy
from sensor_msgs.msg import PointCloud2
import json
import zmq


def callback(data):
    '''pointCloud Callback Function'''
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://172.18.29.153:5555")
    # print data
    s = json.dumps(data) + '---pointCloud'
    # print s
    socket.send(s)
    response = socket.recv()
    print "pointCloud", response


def listener():
    '''pointCloud Subscriber'''
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('pointCloud', anonymous=True)

    rospy.Subscriber("/camera/depth/points", PointCloud2, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
