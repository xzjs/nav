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
cap.set(3, 1920)
cap.set(4, 1080)
context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5555")
camera_req_socket = context.socket(zmq.REQ)
camera_req_socket.connect("tcp://iarobot.org:5557")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
detection_req_socket = context.socket(zmq.REQ)
detection_req_socket.connect("tcp://172.18.29.153:5558")


def talker():
    '''cam Publisher'''
    rospy.init_node('my_cam', anonymous=True)

    i = 0
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        i = i % 5
        name = "/tmp/camera" + str(i) + ".jpg"
        i = i + 1
        # res = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(name, frame)

        # 上传图片
        jpg = open(name, 'rb').read()
        camera_req_socket.send(jpg)
        response = camera_req_socket.recv()
        print 'upload camera success', response, time.time()
        # socket.send_pyobj(frame)

        yolo(name)
        rate.sleep()


def yolo(path):
    socket.send(path)
    message = socket.recv()
    detection_req_socket.send(message)
    response = detection_req_socket.recv()
    print "upload recogniction success", response


if __name__ == '__main__':
    try:
        rospy.loginfo('start camera')
        talker()
    except rospy.ROSInterruptException:
        cap.release()
        cv2.destroyAllWindows()
