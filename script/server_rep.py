#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import threading
import numpy as np
import json
import struct
import base64


def listener():
    context = zmq.Context()
    poller = zmq.Poller()

    # 文件存储路径
    path = "/var/www/server/mapcache/"

    # map
    map_rep_socket = context.socket(zmq.REP)
    map_rep_socket.bind("tcp://*:5555")
    print "map_rep_socket start,port 5555"
    poller.register(map_rep_socket, zmq.POLLIN)

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

    camera_pub_socket = context.socket(zmq.PUB)
    camera_pub_socket.bind("tcp://*:4446")
    print "camera_pub_socket start,port 4446"

    # 识别
    detection_rep_socket = context.socket(zmq.REP)
    detection_rep_socket.bind("tcp://*:5558")
    print "detection_rep_socket start,port 5558"
    poller.register(detection_rep_socket, zmq.POLLIN)

    # 激光数据
    laser_rep_socket = context.socket(zmq.REP)
    laser_rep_socket.bind("tcp://*:5559")
    print "laser_rep_socket start,port 5559"
    poller.register(laser_rep_socket, zmq.POLLIN)

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

    # 人脸识别
    face_rep_socket = context.socket(zmq.REP)
    face_rep_socket.bind("tcp://*:5562")
    print "face_rep_socket start,port 5562"
    poller.register(face_rep_socket, zmq.POLLIN)

    # 激光雷达数据
    slam_rep_socket = context.socket(zmq.REP)
    slam_rep_socket.bind("tcp://*:5563")
    print "slam_rep_socket start,port 5562"
    poller.register(slam_rep_socket, zmq.POLLIN)

    # php发送鼠标点击位置
    php_rep_socket = context.socket(zmq.REP)
    php_rep_socket.bind("tcp://*:7777")
    print 'php_rep_socket start,port 7777'
    poller.register(php_rep_socket, zmq.POLLIN)

    nav_pub_socket = context.socket(zmq.PUB)
    nav_pub_socket.bind("tcp://*:4444")
    print "nav_pub_socket start,port 4444"

    while True:
        try:
            socks = dict(poller.poll())
        except KeyboardInterrupt:
            print "bye"
            break

        if map_rep_socket in socks:
            print "map", time.time()
            recv = map_rep_socket.recv()
            map_rep_socket.send(str(time.time()))
            f = open(path + 'map.png', 'wb')
            f.write(recv)
            f.close()

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
            json.dump(recv, open(path + 'position.json', 'w'))

        if camera_rep_socket in socks:
            print "camera", time.time()
            recv = camera_rep_socket.recv()
            camera_rep_socket.send(str(time.time()))
            f = open(path + 'camera.jpg', 'wb')
            f.write(recv)
            f.close()
            # 发布camera
            camera_pub_socket.send(recv)

        if detection_rep_socket in socks:
            print "dection", time.time()
            recv = detection_rep_socket.recv_json()
            detection_rep_socket.send(str(time.time()))
            json.dump(recv, open(path + 'recognition.json', 'w'))

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

        if laser_rep_socket in socks:
            print "laser", time.time()
            recv = laser_rep_socket.recv_json()
            laser_rep_socket.send(str(time.time()))
            if recv['frame_id'] == '/front_laser_link':
                json.dump(recv['ranges'], open(path + 'f_laser.json', 'w'))
            else:
                json.dump(recv['ranges'], open(path + 'b_laser.json', 'w'))

        if face_rep_socket in socks:
            print "face", time.time()
            recv = face_rep_socket.recv_json()
            face_rep_socket.send(str(time.time()))
            json.dump(recv, open(path + 'face.json', 'w'))

        if slam_rep_socket in socks:
            print "slam", time.time()
            recv = slam_rep_socket.recv_json()
            slam_rep_socket.send(str(time.time()))
            json.dump(recv, open(path + 'slam.json', 'w'))


if __name__ == '__main__':
    listener()
