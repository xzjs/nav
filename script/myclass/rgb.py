#!/usr/bin/python
#-*-coding:utf-8-*-
import zmq


class Rgb:
    '''处理rgb的类'''

    def do(self, data):
        '''处理函数'''
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:7777")  # 往发布接口传输数据
        socket.send(data)
        response = socket.recv()
        print recv()
