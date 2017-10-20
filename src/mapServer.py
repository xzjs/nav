#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''get map'''

import time
import Image
import numpy
import rospy
import zmq
from nav_msgs.srv import GetMap
from PIL import ImageDraw
from geometry_msgs.msg import Pose


context = zmq.Context()
socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5555")
socket.connect("tcp://172.18.29.153:5555")


def saveImage(map, position):
    rospy.loginfo("saveImage")
    print position
    narray = numpy.array(map.data, dtype='int8')  # 转换为array数组
    for i in range(len(narray)):
        if narray[i] == 0:
            narray[i] = 255
        elif narray[i] == 100:
            narray[i] = 0
        elif narray[i] == -1:
            narray[i] = 150
    img = Image.frombytes(
        'L', (map.info.height, map.info.width), narray)  # 转换为灰度图
    # img = img.resize((800, 800))  # 调整大小为400×400
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    draw = ImageDraw.Draw(img)
    point = ((map.info.origin.position.x - position.position.x) * -20,
             (map.info.origin.position.y + position.position.y) * -20)
    draw.ellipse((point[0] - 5, point[1] - 5, point[0] +
                  5, point[1] + 5), 'black', 'white')
    # img.show()
    img.save('/tmp/map.png')  # 保存地图数据
    f = open('/tmp/map.png', 'rb')
    data = f.read() + '----' + str(map.header.stamp) + '----' + \
        str(map.info.origin.position.x) + '----' + \
        str(map.info.origin.position.y)
    socket.send(data)


def mapService(position):
    '''获取地图'''
    try:
        getMap = rospy.ServiceProxy("dynamic_map", GetMap)  # 获取服务
        map = getMap().map  # 获取地图数据
        saveImage(map, position)  # 保存地图数据
    except rospy.ServiceException, e:
        print "service call failed %s" % e


def getPosition():
    '''监听小车坐标'''
    rospy.Subscriber("/robot_pose", Pose, mapService)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node('my_map')
    rospy.wait_for_service("dynamic_map")
    getPosition()
