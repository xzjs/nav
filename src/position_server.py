#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import math
import time

import rospy
import zmq
from geometry_msgs.msg import Pose

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://172.18.29.153:5556")
# socket.connect("tcp://127.0.0.1:5555")


def callback(data):
    p = dict(position=dict(x=data.position.x, y=data.position.y, z=data.position.z), orientation=dict(
        x=data.orientation.z, y=data.orientation.y, z=data.orientation.z, w=data.orientation.w), time=time.time())
    q = p["orientation"]  # 四元数
    angle = math.atan2(2 * (q['w'] * q['z'] + q['x'] * q['y']),
                       1 - 2 * (q['y'] * q['y'] + q['z'] * q['z'])) * -180 / math.pi - 90
    # angle = math.atan2(2 * (q['w'] * q['x'] + q['y'] * q['z']),
    #                    1 - 2 * (q['x'] * q['x'] + q['y'] * q['y'])) * 180 / math.pi - 90
    # angle = math.asin(2 * (q['w'] * q['x'] - q['y']
    #                        * q['z'])) * 180 / math.pi - 90
    p['angle'] = angle
    rospy.loginfo(p)
    socket.send_json(p)
    response = socket.recv()
    print "position", response


def listener():
    rospy.init_node('position_listener')
    rospy.Subscriber("/robot_pose", Pose, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
