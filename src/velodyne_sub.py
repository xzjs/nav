#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''velodyne ROS Node'''
import rospy
from struct import *
import json
import numpy as np
import math
import StringIO

from sensor_msgs.msg import PointCloud2

# 启动命令：roslaunch velodyne_pointcloud VLP16_points.launch

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://172.18.29.153:5556")


def callback(data):
    '''velodyne Callback Function'''
    width = data.width  # 激光点的数目
    # with open('/tmp/data', 'wb') as f1:
    #     f1.write(data.data)
    #     print 'ok'
    # with open('/tmp/data', 'rb') as f2:
    f2 = StringIO.StringIO(data.data)
    data = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    results = []
    indexs = [15, 13, 11, 9, 7, 5, 3, 1, 14, 12,
              10, 8, 6, 4, 2, 0]  # 激光雷达的顺序，从说明书上查到的
    for i in range(0, width):
        (x, y, z) = unpack("fff", f2.read(12))
        f2.seek(8, 1)
        ring = unpack("I", f2.read(4))
        f2.seek(8, 1)
        rotation = round(math.atan2(y, x), 2)
        data[ring[0]].append(
            {'x': x, 'y': y, 'z': z, 'rotation': rotation})
        # print (x, y, z), str(ring), str(rotation)
    for i in range(0, len(indexs)):
        index = indexs[i]
        data[index] = sorted(
            data[index], key=lambda point: point['rotation'])
        if i > 0:
            for j in range(0, len(data[index - 1])):
                result = get_points(
                    data[index - 1][j], data[index - 1][j + 1:], data[index])
                if result is None:
                    continue
                results.append(result)
                print result

    socket.send_json(results)
    response = socket.recv()
    print "slam", response


def get_point(point, points):
    '''获取与给定点最相近的一个点'''
    for p in points:
        if p['rotation'] == point['rotation']:
            return p
        if p['rotation'] > point['rotation']:
            return None


def get_points(point, points1, points2):
    '''获取构成三角面的三个点'''
    result1 = get_point(point, points1)
    result2 = get_point(point, points2)
    if result1 is None or result2 is None:
        return None
    return [point, result1, result2]


def listener():
    '''velodyne Subscriber'''
    rospy.init_node('velodyne', anonymous=True)
    rospy.Subscriber("velodyne_points", PointCloud2, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
