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
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('frame', gray)
        # res = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_CUBIC)
        # cv2.imwrite("/tmp/camera.jpg", frame)
        # f = open('/tmp/camera.jpg', 'rb')  # 读取摄像头图片
        # data = f.read() + '---' + 'cam'
        # socket.send(data)
        img_encode = cv2.imencode('.jpg', frame)[1]
        data_encode = np.array(img_encode)
        str_encode = data_encode.tostring()
        rospy.loginfo(str(time.time()))
        socket.send(str_encode)
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.loginfo('start camera')
        talker()
    except rospy.ROSInterruptException:
        cap.release()
        cv2.destroyAllWindows()
