#!/usr/bin/env python
'''scan ROS Node'''

import zmq
import time


def callback(data):
    '''scan Callback Function'''
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)


def listener():
    '''scan Subscriber'''
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:5559")
    # socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, '')
    print("waiting laser scan,listen 5559")

    while True:
        recv = socket.recv()
        f = open('../map/laser.png', 'wb')
        f.write(recv)
        f.close()
        print 'ok,time ', time.time()


if __name__ == '__main__':
    listener()
