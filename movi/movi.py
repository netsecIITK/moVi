# -*- coding: utf-8 -*-
"Contains initialization code"

import numpy as np
import struct
import sys
import threading

from multiprocessing import Process
from crypto.aes import Aes
from image.format import PacketFormat
from image.webcam import Webcam
from image.frame import FrameDisplay
from image.encodings import JpegEncoding
from image.logging import Logging
from network.udpclient import UDPclient
from network.tcpserver import TCPserver
from network.tcpclient import TCPclient


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
        if mode != "SERVER" and mode != "CLIENT":
            print("Wrong mode")
            exit(1)

        # Set this to whichever encoding you want to test
        self.img_format = JpegEncoding(70)
        self.packetFormat = PacketFormat()
        self.logging = Logging()
        self.regionSize = 150

        if mode == "SERVER":
            print("Running as server")
            tcpserver = TCPserver(port, host)
            for connection in tcpserver.connection_information(3000):
                # For every connection to tcpserver
                print("Got connection from: {}:{}"
                      .format(connection[0], connection[1][1]))

                self.signing = Aes(connection[1][0])

                udp_port = connection[1][1]
                udp_host = connection[0]

                # Bind to a socket
                self.network_client = UDPclient(3000)

                # It has to talk to the negotiated port
                self.network_client.update((udp_host, udp_port))

                # Begin sending data
                # self.sender_single()
                self.runner("SERVER")

            # Finally close TCP
            tcpserver.close()

        else:
            print("Running as client")
            # Talk to target TCP process
            tcpclient = TCPclient(port, host)

            # Get the secret key and udp_port for video from TCP
            key, udp_port = tcpclient.get_information(2000)
            tcpclient.close()

            # Bind to a UDP port to talk
            self.network_client = UDPclient(2000)
            self.network_client.update((host, udp_port))
            self.signing = Aes(key)

            # Begin receiving
            # self.receiver_single()
            self.runner("CLIENT")

    def runner(self, frame_name):
        self.frame_name = frame_name
        # t1 = threading.Thread(target=self.send_state)
        # t2 = threading.Thread(target=self.recv_state)
        t1 = Process(target=self.send_state)
        t2 = Process(target=self.recv_state)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def sender_single(self):
        self.frame_name = "SENDER"
        self.send_state()

    def receiver_single(self):
        self.frame_name = "RECEIVER"
        self.recv_state()

    def send_state(self):
        ret = True
        display = FrameDisplay('{}: Sending frame'.format(self.frame_name))
        # if self.frame_name == "CLIENT":
        #     return 0
        self.cam = Webcam()
        while ret:
            ret, frame = self.cam.getFrame()
            if ret:
                ret = display.showFrame(frame)
                for x in range(0, 450, self.regionSize):
                    for y in range(0, 600, self.regionSize):
                        frame_data = self.img_format.encode(
                            frame[x:min(x + self.regionSize, 450),
                                  y:min(y + self.regionSize, 600)])
                        packet_data = self.packetFormat.pack(
                            x, y, self.signing.sign(frame_data), frame_data)

                        self.network_client.send(packet_data)
                        self.logging.log(("Sent frame ", x, " ", y,
                                          "of length", len(packet_data)))

    def recv_state(self):
        matrix_img = np.zeros((480, 640, 3), dtype=np.uint8)
        display = FrameDisplay('{}: Receiving frame'.format(self.frame_name))
        ret = True
        while ret:
            data, new_addr = self.network_client.recv()
            x, y, sign, frame_data = self.packetFormat.unpack(data)

            # Check validity of packet
            if self.signing.check_sign(sign, frame_data):
                self.logging.log((x, " ", y,
                                  "Got frame of length ", len(data)))
                matrix_img[x:min(x + self.regionSize, 450),
                           y:min(y + self.regionSize, 600)] = (
                               self.img_format.decode(frame_data))
                
                ret = display.showFrame(matrix_img)

                # Update the latest address
                # Should be handled inside recv
                self.network_client.update(new_addr)

# Begin execution
if len(sys.argv) < 4:
    print("Usage: python movi.py SERVER|CLIENT host port")
    exit(1)

MoVi(sys.argv[1], int(sys.argv[3]), sys.argv[2])
