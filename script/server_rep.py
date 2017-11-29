#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import threading
import numpy as np
import json
import struct
import base64
import redis


def listener():
    context = zmq.Context()
    poller = zmq.Poller()

    # map
    map_rep_socket = context.socket(zmq.REP)
    map_rep_socket.bind("tcp://*:5555")
    print "map_rep_socket start,port 5555"

    # 坐标
    position_rep_socket = context.socket(zmq.REP)
    position_rep_socket.bind("tcp://*:5556")
    print "position_rep_socket start,port 5556"
    poller.register(position_rep_socket, zmq.POLLIN)

    # camera
    camera_rep_socket = context.socket(zmq.REP)
    camera_rep_socket.bind("tcp://*:5557")
    print "camera_rep_socket start,port 5557"
    poller.register(camera_rep_socket, zmq.POLLIN)

    # 识别
    detection_rep_socket = context.socket(zmq.REP)
    detection_rep_socket.bind("tcp://*:5558")
    print "detection_rep_socket start,port 5558"
    poller.register(detection_rep_socket, zmq.POLLIN)

    # 点云
    point_cloud_rep_socket = context.socket(zmq.REP)
    point_cloud_rep_socket.bind("tcp://*:5560")
    print "point_cloud_rep_socket start,port 5560"
    poller.register(point_cloud_rep_socket, zmq.POLLIN)

    point_cloud_pub_socket = context.socket(zmq.PUB)
    point_cloud_pub_socket.bind("tcp://*:4445")
    print "point_cloud_pub_socket start,port 4445"

    # 点云处理结果
    point_result_rep_socket = context.socket(zmq.REP)
    point_result_rep_socket.bind("tcp://*:5561")
    print "point_result_rep_socket start,port 5561"
    poller.register(point_result_rep_socket, zmq.POLLIN)

    # php发送鼠标点击位置
    php_rep_socket = context.socket(zmq.REP)
    php_rep_socket.bind("tcp://*:7777")
    print 'php_rep_socket start,port 7777'
    poller.register(php_rep_socket, zmq.POLLIN)

    nav_pub_socket = context.socket(zmq.PUB)
    nav_pub_socket.bind("tcp://*:4444")
    print "nav_pub_socket start,port 4444"

    # redis
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            print "bye"
            break

        if point_cloud_rep_socket in socks:
            print "point cloud", time.time()
            recv = point_cloud_rep_socket.recv_pyobj()
            point_cloud_rep_socket.send(str(time.time()))
            # 将消息发布出去
            point_cloud_pub_socket.send_pyobj(recv)

        if position_rep_socket in socks:
            print "position", time.time()
            recv = position_rep_socket.recv_json()
            position_rep_socket.send(str(time.time()))
            json.dump(recv, open('/var/www/server/map/position.json', 'w'))

        if camera_rep_socket in socks:
            print "camera", time.time()
            recv = camera_rep_socket.recv()
            camera_rep_socket.send(str(time.time()))
            base_str = base64.b64encode(recv)
            r.set('img',base_str)

        if detection_rep_socket in socks:
            print "dection", time.time()
            recv = detection_rep_socket.recv()
            detection_rep_socket.send(str(time.time()))
            json.dump(recv, open('/var/www/server/map/recognition.json', 'w'))

        if point_result_rep_socket in socks:
            print "point result", time.time()
            recv = point_result_rep_socket.recv_json()
            print recv
            point_result_rep_socket.send_json(recv)  # 暂时先将结果返回回去

        if php_rep_socket in socks:
            print "php", time.time()
            recv = php_rep_socket.recv()
            php_rep_socket.send(str(time.time()))

            nav_pub_socket.send(recv)


if __name__ == '__main__':
    listener()
