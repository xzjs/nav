#!/usr/bin/env python
import zmq
import time
import cv2


def listener():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://192.168.31.4:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting camera")
    # req_socket = context.socket(zmq.REQ)
    # req_socket.connect("tcp://172.18.29.153:5555")

    while True:
        recv = socket.recv()
        f = open('/tmp/camera.jpg', 'wb')
        f.write(recv)
        f.close()
        image=cv2.imread("/tmp/camera.jpg")
        res = cv2.resize(image, (320,240), interpolation=cv2.INTER_AREA)
        cv2.imwrite("/tmp/camera_min.jpg")
        print 'ok,time ', time.time()


if __name__ == '__main__':
    listener()
