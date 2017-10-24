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
        message = get_socket.recv()
        print message
        send_socket.send(message)
        get_socket.send('ok')


if __name__ == '__main__':
    get_goal()
