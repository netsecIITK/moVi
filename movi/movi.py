# -*- coding: utf-8 -*-
"Contains initialization code"

import cv2
import numpy as np
import sys
import time
from network.udpserver import UDPserver
from network.udpclient import UDPclient
from image.webcam import Webcam
from image.pack import MoViPack
from image.unpack import MoViUnpack
from image.frame import FrameDisplay


class MoVi:
    "Begin of moVi"

    def __init__(self, mode, port, host):
        if mode == "SERVER":
            self.server = UDPserver(port, host)
        elif mode == "CLIENT":
            self.client = UDPclient(port, host)
        else:
            print("Wrong mode")
            exit(1)

        if mode == "SERVER":
            print("Running as server")

            self.server.get_hello()

            self.cam = Webcam()
            self.pickler = MoViPack()
            self.display = FrameDisplay('server_frame')

            ret = True
            while ret:
                ret, frame = self.cam.getFrame()

                if ret:
                    # self.display.showFrame(frame)
                    self.cam.showFrame(frame, 'server_frame')
                    print("Got a FRAME")
                    for x in range(0, 450, 50):
                        for y in range(0, 600, 50):
                            frame_data = bytearray(
                                bytes([(y//50)*10 + (x//50)]))
                            frame_data.extend(cv2.imencode(
                                '.jpg', frame[x:min(x+50, 450),
                                              y:min(y+50, 600)],
                                [cv2.IMWRITE_JPEG_QUALITY, 70])[1])
                            self.server.send(frame_data)
                            print("Sent frame ", x, " ", y)
                            print("Length ", len(frame_data))

            self.cam.close()
        else:
            print("Running as client")
            self.unpickler = MoViUnpack()
            self.display = FrameDisplay('client_frame')

            self.client.send_hello()

            matrix_img = np.zeros((480, 640, 3), dtype=np.uint8)

            ret = True
            while ret:
                # for x in range(0, 450, 50):
                #     for y in range(0, 600, 50):
                data = self.client.recv()
                index = int.from_bytes([data[0]], 'little')
                print(index)
                x = (index % 10)*50
                y = ((index)//10)*50
                print(x, " ", y)

                frame_data = np.fromstring(data[1:], np.uint8)
                print("Got frame")
                print("Length ", len(data))
                matrix_img[x:min(x+50, 450),
                           y:min(y+50, 600)] = cv2.imdecode(
                               frame_data, cv2.IMREAD_COLOR)

                cv2.imshow('client_frame', matrix_img)
                cv2.waitKey(1)


# Begin execution
if len(sys.argv) < 4:
    print("Usage: python movi.py SERVER|CLIENT host port")
    exit(1)

MoVi(sys.argv[1], int(sys.argv[3]), sys.argv[2])
