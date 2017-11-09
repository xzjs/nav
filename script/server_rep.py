#!/usr/bin/env python
# -*- coding:utf-8 -*-
import zmq
import time
import threading
import numpy as np
import json
import myclass


class Factory:
    def getClass(self, type):
        if type == 'rgb':
            return myclass.rgb.Rgb()
        return None


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
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("service start,listening 5555")

    factory = Factory()

    nameDict = {
        'map': 'map.png',
        'cam': 'camera.jpg',
        'scan': 'laser.json',
        'position': 'position.json',
        'recognition': 'recognition.json',
        'pointCloud': ''
    }

    while True:
        recv = socket.recv()
        socket.send(str(time.time()))
        data = recv.split('---')
        if data[1] in nameDict:
            obj = factory.getClass(data[1])
            if obj != None:
                obj.do(data[0])
            else:
                print data[1]
                func = 'wb'  # 读写方式
                if data[1] == 'position':
                    func = 'w'
                t = threading.Thread(target=savefile, args=(
                    nameDict[data[1]], data[0], func,))
                t.setDaemon(True)
                t.start()


if __name__ == '__main__':
    listener()
