#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import threading
import numpy as np
import json
import struct


def savefile(path, data, type):
    if path == "laser.json":
        laser = json.loads(data)
        if laser['frame_id'] == "/front_laser_link":
            path = "f_laser.json"
        else:
            path = "b_laser.json"
        data = json.dumps(laser['ranges'])
    f = open('/var/www/server/map/' + path, type)
    f.write(data)
    f.close()
    print path + ' ok,time ', time.time()


def listener():
    context = zmq.Context()

    # map
    map_rep_socket = context.socket(zmq.REP)
    map_rep_socket.bind("tcp://*:5555")
    print "map_rep_socket start,port 5555"

    # 坐标
    position_rep_socket = context.socket(zmq.REP)
    position_rep_socket.bind("tcp://*:5556")
    print "position_rep_socket start,port 5556"

    # camera
    camera_rep_socket = context.socket(zmq.REP)
    camera_rep_socket.bind("tcp://*:5557")
    print "camera_rep_socket start,port 5557"

    # 点云
    point_cloud_rep_socket = context.socket(zmq.REP)
    point_cloud_rep_socket.bind("tcp://*:5560")
    print "point_cloud_rep_socket start,port 5560"
    point_cloud_pub_socket = context.socket(zmq.PUB)
    point_cloud_pub_socket.bind("tcp://*:4445")
    print "point_cloud_pub_socket start,port 4445"

    poller = zmq.Poller()
    poller.register(point_cloud_rep_socket, zmq.POLLIN)
    poller.register(position_rep_socket, zmq.POLLIN)
    poller.register(camera_rep_socket, zmq.POLLIN)

    # nameDict = [
    #     'map.png',
    #     'camera.jpg',
    #     'laser.json',
    #     'position.json',
    #     'recognition.json',
    #     'pointCloud'
    # ]

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
            print "camera",time.time()
            

        # recv = socket.recv()
        # socket.send(str(time.time()))
        # temp = ''.join(recv[0:4])
        # data = struct.unpack('i', temp)[0]
        # print data
        # if data < len(nameDict):
        #     if data == 0:
        #         pass
        #     if data == 1:
        #         pass
        #     if data == 2:
        #         pass
        #     if data == 3:
        #         pass
        #     if data == 4:
        #         pass
        #     if data == 5:
        #         point_cloud=''.join(recv[4:])
        #         point_cloud_pub_socket.send

            # print data[1]
            # func = 'wb'  # 读写方式
            # if data[1] == 'position':
            #     func = 'w'
            # t = threading.Thread(target=savefile, args=(
            #     nameDict[data[1]], data[0], func,))
            # t.setDaemon(True)
            # t.start()


if __name__ == '__main__':
    listener()
