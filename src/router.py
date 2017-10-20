#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''router ROS Node'''
# license removed for brevity
import rospy
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5555")
socket.connect("tcp://172.18.29.153:5555")


def talker():
    '''cam Publisher'''
    # pub = rospy.Publisher('camera_data', String, queue_size=10)
    rospy.init_node('my_cam', anonymous=True)
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('frame', gray)
        res = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("/tmp/camera.jpg", res)
        f = open('/tmp/camera.jpg', 'rb')  # 读取摄像头图片
        data = f.read() + '---' + 'cam'
        socket.send(data)
        rospy.loginfo('upload success')
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.loginfo('start canera')
        talker()
    except rospy.ROSInterruptException:
        cap.release()
        cv2.destroyAllWindows()
