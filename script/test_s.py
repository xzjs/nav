import time
import zmq
import Image


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    while True:
        img = open('../map/map.png', 'rb')
        # socket.send([img.read(), time.time()])
        socket.send(img.read())
        img.close()
        time.sleep(5)


if __name__ == '__main__':
    main()
