#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''cam ROS Node'''
# license removed for brevity
import rospy

import cv2
import numpy as np
import pickle
import zmq
import time

cap = cv2.VideoCapture(0)
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
camera_req_socket = context.socket(zmq.REQ)
camera_req_socket.connect("tcp://iarobot.org:5557")


def talker():
    '''cam Publisher'''
    rospy.init_node('my_cam', anonymous=True)

    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        res = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite("/tmp/cam_small.jpg", res)

        # 上传图片
        jpg = open('/tmp/cam_small.jpg', 'rb').read()
        camera_req_socket.send(jpg)
        response = camera_req_socket.recv()
        print 'upload camera success', response, time.time()
        socket.send_pyobj(frame)
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.loginfo('start camera')
        talker()
    except rospy.ROSInterruptException:
        cap.release()
        cv2.destroyAllWindows()
