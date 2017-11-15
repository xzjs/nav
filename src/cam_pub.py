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


def talker():
    '''cam Publisher'''
    rospy.init_node('my_cam', anonymous=True)

    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        img_encode = cv2.imencode('.jpg', frame)[1]
        socket.send(img_encode)
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.loginfo('start camera')
        talker()
    except rospy.ROSInterruptException:
        cap.release()
        cv2.destroyAllWindows()
