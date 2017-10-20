#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''cam ROS Node'''
import pickle

import cv2
import numpy as np
import roslib
# license removed for brevity
import rospy
from sensor_msgs.msg import CompressedImage

cap = cv2.VideoCapture(0)
# context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5555")
# socket.connect("tcp://192.168.31.5:5555")


def talker():
    '''cam Publisher'''
    pub = rospy.Publisher('/camera_data', CompressedImage, queue_size=10)

    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('frame', gray)
        res = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_CUBIC)
        # cv2.imwrite("/tmp/camera.jpg", res)
        # f = open('/tmp/camera.jpg', 'rb')  # 读取摄像头图片
        # data = f.read() + '---' + 'cam'
        # socket.send(data)
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', res)[1]).tostring()
        pub.publish(msg)
        rospy.loginfo('upload success')
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('my_camera', anonymous=True)
        rospy.loginfo('start canera')
        talker()
    except rospy.ROSInterruptException:
        cap.release()
        cv2.destroyAllWindows()
