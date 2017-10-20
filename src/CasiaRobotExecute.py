#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import threading


def savefile(path, data, type):
    f = open('../map/' + path, type)
    f.write(data)
    f.close()
    print path + ' ok,time ', time.time()


def listener():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    # 5555用来接受
    # socket.bind("tcp://*:5555")
    socket.connect("tcp://127.0.0.1:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("service start,listening 5555")

    # 5557用来请求图像识别
    req_socket = context.socket(zmq.PUB)
    req_socket.bind("tcp://*:5557")

    nameDict = {
        'map': 'map.png',
        'cam': 'camera.jpg',
        'scan': 'laser.png',
        'position': 'position.json',
        'recognition': 'recognition.json'
    }

    while True:
        recv = socket.recv()
        data = recv.split('---')
        if data[1] in nameDict:
            # print data[1]
            func = 'wb'  # 读写方式
            if data[1] == 'position':
                func = 'w'
            if data[1] == 'cam':
                req_socket.send(data[0])
                # print 'data send success'
            if data[1] == 'recognition':
                print data[0]
            t = threading.Thread(target=savefile, args=(
                nameDict[data[1]], data[0], func,))
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    listener()
