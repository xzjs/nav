#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import cv2
import detection
import rospy
import numpy as np
import base64
import sys
import signal


def quit(signum, frame):
    sys.exit()


def listener():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.31.4:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting camera")
    # 上传摄像头数据
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://172.18.29.153:5557")
    # 上传识别结果
    detection_req_socket = context.socket(zmq.REQ)
    detection_req_socket.connect("tcp://172.18.29.153:5558")

    net, classes = detection.get_net()

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    while True:
        # 接收消息存储图片
        recv = socket.recv_pyobj()
        # cv2.imwrite("/tmp/cam_big.jpg", res)

        # # 压缩图片
        # res = cv2.resize(recv, (320, 240), interpolation=cv2.INTER_AREA)
        # cv2.imwrite("/tmp/cam_small.jpg", res)

        # # 上传图片
        # jpg = open('/tmp/cam_small.jpg', 'rb').read()
        # req_socket.send(jpg)
        # response = req_socket.recv()
        # print 'upload camera success', response

        # 识别图片
        img = cv2.imread("/tmp/cam_big.jpg")
        result = detection.recognize(net, classes, img)
        if result:
            # print result
            detection_req_socket.send(result)
            response = detection_req_socket.recv()
            print "upload recogniction success", response


if __name__ == '__main__':
    try:
        rospy.init_node('my_camera', anonymous=True)
        listener()
    except KeyboardInterrupt:
        print 'bye'
