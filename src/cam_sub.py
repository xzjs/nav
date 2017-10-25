#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import cv2
import detection
import rospy
import numpy as np


def listener():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.31.4:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting camera")
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://172.18.29.153:5555")
    # req_socket.connect("tcp://localhost:5555")
    net, classes = detection.get_net()

    while True:
        # 接收消息存储图片
        recv = socket.recv()
        frame=cv2.imdecode(np.fromstring(recv,np.uint8))
        gray = cv2.cvtColor(recv, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        # f = open('/tmp/camera.jpg', 'wb')
        # f.write(recv)
        # f.close()

        # # 发布图片
        # result = detection.recognize(net, classes)
        # if result:
        #     # print result
        #     req_socket.send(result + "---recognition")
        #     response = req_socket.recv()
        #     print "upload recogniction success", response

        # # 压缩图片
        # image = cv2.imread("/tmp/camera.jpg")
        # res = cv2.resize(image, (320, 240), interpolation=cv2.INTER_AREA)
        # cv2.imwrite("/tmp/camera_min.jpg", res)

        # # 上传图片
        # f = open('/tmp/camera_min.jpg', 'rb')  # 读取摄像头图片
        # data = f.read() + '---cam'
        # req_socket.send(data)
        # response = req_socket.recv()
        # print 'upload camera success', response


if __name__ == '__main__':
    rospy.init_node('my_camera', anonymous=True)
    listener()
