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
import threading
import subprocess
import json

context = zmq.Context()
net, classes = detection.get_net()

data = [{'name': '无双公子', 'path': '/home/ros/htb/src/nav/bin/distinguish/pics/2-1.jpg'}]


class Face:
    '''人脸'''

    def __init__(self, name='', area=[0, 0, 0, 0], probability=0.5):
        self.name = name
        self.area = area
        self.probability = probability


def listener():
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.31.4:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting camera")

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)
    while True:
        # 接收消息存储图片
        recv = socket.recv_pyobj()
        cv2.imwrite("/tmp/cam_big.jpg", recv)

        threads = []
        # t1 = threading.Thread(target=recognize, args=(recv,))
        # threads.append(t1)
        # t2 = threading.Thread(target=distinguish, args=('/tmp/cam_big.jpg',))
        # threads.append(t2)

        # for t in threads:
        #     t.setDaemon(True)
        #     t.start

        recognize(recv)
        distinguish('/tmp/cam_big.jpg')


def recognize(recv):
    '''物体识别'''
    detection_req_socket = context.socket(zmq.REQ)
    detection_req_socket.connect("tcp://172.18.29.153:5558")
    result = detection.recognize(net, classes, recv)
    if result:
        print result
        detection_req_socket.send(result)
        response = detection_req_socket.recv()
        print "upload recogniction success", response


def distinguish(img_path):
    '''人脸识别'''
    face = Face()
    for item in data:
        array = tool(img_path, item['path'])
        if array[5] > face.probability:
            face = Face(item['name'], array[1:5], array[5])
    face_req_socket = context.socket(zmq.REQ)
    face_req_socket.connect("tcp://172.18.29.153:5562")
    face_req_socket.send_json(face.__dict__)
    response = face_req_socket.recv()
    print "upload face success", response


def tool(img_path, people_img_path):
    str = "cd /home/ros/htb/src/nav/bin/distinguish && ./test " + \
        img_path + " " + people_img_path
    result = subprocess.check_output(str, shell=True)
    array = result.split('|')
    print array[1], array[2], array[3], array[4], array[5]
    return array


def quit(signum, frame):
    sys.exit()


if __name__ == '__main__':
    try:
        rospy.init_node('my_camera', anonymous=True)
        listener()
    except KeyboardInterrupt:
        print 'bye'
