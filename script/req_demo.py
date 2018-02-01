#!/usr/bin/env python
# -*- coding:utf-8 -*-

import zmq
import cv2
import numpy as np
import json
import sys
import ft2

reload(sys)
sys.setdefaultencoding('utf8')

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

dict = json.load(open('../resource/dict.json'))

path = '/tmp/test.jpg'

while True:
    ret, frame = cap.read()
    cv2.imwrite(path, frame)

    socket.send(path)
    message = socket.recv()
    print message
    data = json.loads(message)
    for val in data:
        cv2.rectangle(frame, (val['left'], val['top']),
                      (val['right'], val['bot']), (0, 0, 255), 2)
        name = dict[unicode.encode(val['name'])]
        print name
        cv2.putText(frame, name, (val['left'] + 10, val['top'] + 10),
                    cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255), 2, 1)

    cv2.imshow("capture", frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
