#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import zmq
import time
import json

context = zmq.Context()
get_socket = context.socket(zmq.REP)  # 接收php发送的坐标
get_socket.bind("tcp://*:7777")
send_socket = context.socket(zmq.PUB)  # 下发坐标
send_socket.bind("tcp://*:5556")


def get_goal():
    while True:
        recv = get_socket.recv()
        get_socket.send(str(time.time()))
        data = recv.split('---')
        send_socket.send("%s %s" % (data[1], data[0]))
        get_socket.send('ok')


if __name__ == '__main__':
    get_goal()
