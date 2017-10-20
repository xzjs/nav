#!/usr/bin/env python
'''speed ROS Node'''
import rospy
from geometry_msgs.msg import Twist
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5558")


def callback(data):
    '''speed Callback Function'''
    # rospy.loginfo(data)
    linear = data.linear.x
    angular = data.angular.z
    s = str(linear) + ',' + str(angular)
    print s
    socket.send(s)


def listener():
    '''speed Subscriber'''
    rospy.init_node('speed', anonymous=True)

    rospy.Subscriber("/cmd_vel", Twist, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
