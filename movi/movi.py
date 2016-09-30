# -*- coding: utf-8 -*-
"Contains initialization code"

import numpy as np
import struct
import sys
from network.udpserver import UDPserver
from network.udpclient import UDPclient
from image.webcam import Webcam
from image.frame import FrameDisplay
from image.encodings import JpegEncoding


class MoVi:
    "Begin of moVi"

    def integer_bytes_encode(self, ints):
        b = bytearray()
        for i in ints:
            # < is for little endian
            # H is for unsigned short (16 bits)
            b += struct.pack("<H", i)
        return b

    def integer_bytes_decode(self, byte_array):
        repr(byte_array)
        return struct.unpack("<H", byte_array)[0]

    def __init__(self, mode, port, host):
        if mode == "SERVER":
            self.server = UDPserver(port, host)
        elif mode == "CLIENT":
            self.client = UDPclient(port, host)
        else:
            print("Wrong mode")
            exit(1)

        # Set this to whichever encoding you want to test
        self.img_format = JpegEncoding(70)

        if mode == "SERVER":
            print("Running as server")

            # Wait for an initial handshake with the client
            self.server.get_hello()

            self.cam = Webcam()
            self.display = FrameDisplay('server_frame')

            ret = True
            while ret:
                ret, frame = self.cam.getFrame()

                if ret:
                    ret = self.display.showFrame(frame)
                    for x in range(0, 450, 50):
                        for y in range(0, 600, 50):
                            frame_data = self.integer_bytes_encode([x, y])
                            frame_data.extend(self.img_format.encode(
                                frame[x:min(x+50, 450), y:min(y+50, 600)]))
                            self.server.send(frame_data)
                            print("Sent frame ", x, " ", y)
                            print("Length ", len(frame_data))

            self.cam.close()
            self.display.close()

        else:
            print("Running as client")
            self.display = FrameDisplay('client_frame')

            self.client.send_hello()

            matrix_img = np.zeros((480, 640, 3), dtype=np.uint8)

            ret = True
            while ret:
                data = self.client.recv()
                x = self.integer_bytes_decode(data[0:2])
                y = self.integer_bytes_decode(data[2:4])
                print(x, " ", y)

                frame_data = np.fromstring(data[4:], np.uint8)
                print("Got frame of length ", len(data))
                matrix_img[x:min(x+50, 450),
                           y:min(y+50, 600)] = (self.
                                                img_format.decode(frame_data))

                ret = self.display.showFrame(matrix_img)

            self.display.close()


# Begin execution
if len(sys.argv) < 4:
    print("Usage: python movi.py SERVER|CLIENT host port")
    exit(1)

MoVi(sys.argv[1], int(sys.argv[3]), sys.argv[2])
