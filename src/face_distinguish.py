#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''人脸识别'''

import time
import Image
import numpy
import rospy
import zmq
from nav_msgs.msg import OccupancyGrid
import json
import subprocess


context = zmq.Context()
socket = context.socket(zmq.REQ)
# socket.connect("tcp://127.0.0.1:5555")
socket.connect("tcp://172.18.29.153:5555")


def mapService(map):
    '''获取并将地图存入zmq'''
    max_value = max(map.data)  # 检测是否是脏数据，脏数据的最大值为96
    if max_value < 100:
        return
    rospy.loginfo('get map data')
    narray = numpy.array(map.data, dtype='int8')  # 转换为array数组
    # 地图颜色修改
    for i in range(len(narray)):
        if narray[i] == 0:
            narray[i] = 255
        elif narray[i] == 100:
            narray[i] = 0
        elif narray[i] == -1:
            narray[i] = 150

    img = Image.frombytes(
        'L', (map.info.height, map.info.width), narray)  # 转换为灰度图
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save('/tmp/map.png')  # 保存地图数据,转换为png压缩图片大小
    f = open('/tmp/map.png', 'rb')  # 读取地图数据
    data = f.read()
    socket.send(data)
    response = socket.recv()


def getMap():
    '''监听小车地图'''
    rospy.Subscriber("/map", OccupancyGrid, mapService)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('my_face_distinguish')
    result = subprocess.check_output("ls")
    print result
