#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import cv2
import detection
import rospy
import numpy as np
import base64


def listener():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.31.4:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting camera")
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://172.18.29.153:5557")
    # req_socket.connect("tcp://localhost:5555")
    net, classes = detection.get_net()

    while True:
        # 接收消息存储图片
        recv = socket.recv_pyobj()
        cv2.imwrite("test.jpg", recv)

        # # 压缩图片
        # res = cv2.resize(img_decode, (320, 240), interpolation=cv2.INTER_AREA)

        # # 上传图片
        # img_encode = cv2.imencode('.jpg', res)[1]
        # data_encode = np.array(img_encode)
        # req_socket.send(data_encode)
        # response = req_socket.recv()
        # print 'upload camera success', response

        # # 识别图片
        # result = detection.recognize(net, classes, img_decode)
        # if result:
        #     # print result
        #     req_socket.send(result + "---recognition")
        #     response = req_socket.recv()
        #     print "upload recogniction success", response


if __name__ == '__main__':
    rospy.init_node('my_camera', anonymous=True)
    listener()
