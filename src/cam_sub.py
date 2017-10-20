#!/usr/bin/env python
import zmq
import time


def listener():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5558")
    # socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting camera,listen 5558")

    while True:
        recv = socket.recv()
        f = open('../map/camera.jpg', 'wb')
        f.write(recv)
        f.close()
        print 'ok,time ', time.time()


if __name__ == '__main__':
    listener()
