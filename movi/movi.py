# -*- coding: utf-8 -*-
"Contains initialization code"

import numpy as np
import struct
import sys
from crypto.aes import Aes
from image.format import PacketFormat
from image.webcam import Webcam
from image.frame import FrameDisplay
from image.encodings import JpegEncoding
from image.logging import Logging
from network.udpserver import UDPserver
from network.udpclient import UDPclient
from network.packetType import PacketType


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

        key = "abcd"
        packetFormat = PacketFormat()
        signing = Aes(key)

        self.logging = Logging()

        self.regionSize = 100


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
                    for x in range(0, 450, self.regionSize):
                        for y in range(0, 600, self.regionSize):
                            frame_data = self.img_format.encode(
                                frame[x:min(x + self.regionSize, 450),
                                      y:min(y + self.regionSize, 600)])
                            packet_data = packetFormat.pack(
                                x, y, signing.sign(frame_data), frame_data)

                            self.server.send(packet_data)
                            self.logging.log(("Sent frame ", x, " ", y))
                            self.logging.log(("Length ", len(packet_data)))

            self.cam.close()
            self.display.close()

        else:
            print("Running as client")
            self.display = FrameDisplay('client_frame')

            self.client.send_hello()

            matrix_img = np.zeros((480, 640, 3), dtype=np.uint8)

            ret = True
            while ret:
                data, new_addr = self.client.recv()
                x, y, sign, frame_data = packetFormat.unpack(data)

                # Check validity of packet
                if signing.check_sign(sign, frame_data):
                    self.logging.log((x, " ", y))
                    self.logging.log(("Got frame of length ", len(data)))
                    matrix_img[x:min(x + self.regionSize, 450),
                               y:min(y + self.regionSize, 600)] = (self.img_format.
                                                    decode(frame_data))
                    ret = self.display.showFrame(matrix_img)

                    # Update the latest address
                    self.client.update(new_addr)

            self.display.close()


# Begin execution
if len(sys.argv) < 4:
    print("Usage: python movi.py SERVER|CLIENT host port")
    exit(1)

MoVi(sys.argv[1], int(sys.argv[3]), sys.argv[2])
