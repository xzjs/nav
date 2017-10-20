#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''router'''

import zmq

context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)
frontend.bind("tcp://*:5555")
backend.bind("tcp://*:5556")

poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
# poller.register(backend,zmq.POLLOUT)

while True:
    socks = dict(poller.poll)

    if socks.get(frontend) == zmq.POLLIN:
        message = frontend.recv()
        backend.send(message)
