#!/usr/bin/python
#-*-coding:utf-8-*-

import zmq
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://192.168.31.106:5557")
socket.setsockopt(zmq.SUBSCRIBE, '')
while True:
    print socket.recv()
