#!/usr/bin/python
#-*-coding:utf-8-*-

import zmq
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:4445")
socket.setsockopt(zmq.SUBSCRIBE, '')
while True:
    recv = socket.recv_pyobj()
    print recv
