#!/usr/bin/env python
#coding=utf-8
import json

import zmq


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    print("collecting message")
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')

    while True:
        # [image, time] = socket.recv()
        data = socket.recv()
        f = open('test.png', 'wb')
        f.write(data)
        f.close()
        print data
        # print time
        print 'ok'


def test():
    context=zmq.Context()
    socket=context.socket(zmq.SUB)
    socket.connect('tcp://localhost:5557')
    socket.setsockopt(zmq.SUBSCRIBE, '')
    while True:
        message=socket.recv()
        print 'get message'


if __name__ == '__main__':
    # main()
    test()
