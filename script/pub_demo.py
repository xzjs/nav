#!/usr/bin/python
#-*-coding:utf-8-*-

import zmq
import json
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://192.168.31.106:5555")


def pub_message():
    data = [[['a', 123]]]
    json_str = json.dumps(data)  # 识别后的json字符串
    msg = json_str + "---recognition"
    socket.send(msg)


if __name__ == '__main__':
    pub_message()
