#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import zmq
import time
import json


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5556")
    # socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting position")

    while True:
        recv = socket.recv()
        print len(recv)
        name = str(time.time())
        f = open('../map/position.json', 'w')
        f.write(recv)
        f.close()
        print 'save position success' + str(time.time())


if __name__ == '__main__':
    main()
