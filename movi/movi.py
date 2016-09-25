# -*- coding: utf-8 -*-
"Contains initialization code"

import sys
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

            ret = True
            while ret:
                ret, frame = self.cam.getFrame()
                if ret:
                    self.cam.showFrame(frame)
                    # self.server.send(
                    # self.pickler.get_pickles(frame))
                    self.server.send(
                        self.pickler.get_pickles('abcde'))

            self.cam.close()
        else:
            print("Running as client")
            self.unpickler = MoViUnpack()
            self.display = FrameDisplay()

            self.client.send_hello()

            ret = True
            while ret:
                frame_data = self.client.recv()
                # self.display.showFrame(
                # self.unpickler.get_frame(frame_data))
                print(self.unpickler.get_frame(frame_data))


# Begin execution
if len(sys.argv) < 4:
    print("Usage: python movi.py SERVER|CLIENT host port")
    exit(1)

MoVi(sys.argv[1], int(sys.argv[3]), sys.argv[2])
