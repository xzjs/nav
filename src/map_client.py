#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import zmq
import time
import json


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5555")
    # socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting map")

    while True:
        recv = socket.recv()
        # data = json.loads(recv,ensure_ascii=False)
        data = recv.split('----')
        print len(data)
        name = str(time.time())
        f = open('../map/map.png', 'wb')
        f.write(data[0])
        f.close()
        print 'ok,time ', name


if __name__ == '__main__':
    main()
