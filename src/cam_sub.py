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
        nparr = np.fromstring(recv, np.uint8)
        img_decode = cv2.imdecode(nparr, 1)
        cv2.imwrite("test.jpg", img_decode)

        # 发布图片
        result = detection.recognize(net, classes, img_decode)
        if result:
            # print result
            req_socket.send(result + "---recognition")
            response = req_socket.recv()
            print "upload recogniction success", response

        # 压缩图片
        res = cv2.resize(img_decode, (320, 240), interpolation=cv2.INTER_AREA)

        # 上传图片
        img_encode = cv2.imencode('.jpg', res)[1]
        data_encode = np.array(img_encode)
        str_encode = data_encode.tostring()
        req_socket.send(str_encode + "---cam")
        response = req_socket.recv()
        print 'upload camera success', response


if __name__ == '__main__':
    rospy.init_node('my_camera', anonymous=True)
    listener()
