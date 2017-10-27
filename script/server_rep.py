#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import threading
import numpy as np


def savefile(path, data, type):
    f = open('/var/www/server/map/' + path, type)
    f.write(data)
    f.close()
    print path + ' ok,time ', time.time()


def listener():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("service start,listening 5555")

    nameDict = {
        'map': 'map.png',
        'cam': 'camera.jpg',
        'scan': 'laser.json',
        'position': 'position.json',
        'recognition': 'recognition.json'
    }

    while True:
        recv = socket.recv()
        socket.send(str(time.time()))
        data = recv.split('---')
        if data[1] in nameDict:
            # print data[1]
            func = 'wb'  # 读写方式
            if data[1] == 'position':
                func = 'w'
            t = threading.Thread(target=savefile, args=(
                nameDict[data[1]], data[0], func,))
            t.setDaemon(True)
            t.start()


if __name__ == '__main__':
    listener()
