# -*- coding: utf-8 -*-
"Contains initialization code"

import numpy as np
import struct
import sys
import threading
import queue
import cv2
import time

from multiprocessing import Process
from crypto.aes import Aes
from image.format import PacketFormat
from image.webcam import Webcam
from image.frame import FrameDisplay
from image.encodings import JpegEncoding
from image.logging import Logging
from network.udpclient import UDPclient
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

    def __init__(self, mode, broker_ip):
        if mode != "SERVER" and mode != "CLIENT":
            print("Wrong mode")
            exit(1)

        # Set this to whichever encoding you want to test
        self.jpeg_quality = 70
        self.jpeg_lower = 40
        self.jpeg_upper = 85
        self.img_format = JpegEncoding(self.jpeg_quality)
        self.packetFormat = PacketFormat()
        self.logging = Logging()
        self.regionSize = 150
        self.time_last = 0
        self.time_waiting = 0.25
        self.threshold = 280
        self.lower_thresh = 250
        self.upper_thresh = 330

        self.recved_frames = 0

        broker_client = TCPclient(8500, broker_ip)
        self.network_client = UDPclient(3000)
        self.network_client.update((broker_ip, 3500))
        self.network_client.send("ping".encode())
        self.network_client_ack = UDPclient(4000)
        self.network_client_ack.update((broker_ip, 4500))
        self.network_client_ack.send("ping".encode())

        (other_ip, tcp_port,
         udp_port1, udp_port2) = broker_client.udp_hole_mapping()

        self.udp_host = other_ip
        self.key = "abcd"

        broker_client.close()

        if mode == "SERVER":
            print("Running as server")
            # tcpserver = TCPserver(port, host)
            # for connection in tcpserver.connection_information(3000):
            #     # For every connection to tcpserver
            #     print("Got connection from: {}:{}"
            #           .format(connection[0], connection[1][1]))

            self.signing = Aes(self.key)

            self.network_client.update((self.udp_host, udp_port1))

            self.network_client_ack.update((self.udp_host, udp_port2))
            # Begin sending data
            # self.sender_single()
            self.runner("SERVER")

            # Finally close TCP
            # tcpserver.close()

        else:
            print("Running as client")
            # Talk to target TCP process
            # tcpclient = TCPclient(tcp_port, self.udp_host)

            # Get the secret key and udp_port for video from TCP
            # key, udp_port = tcpclient.get_information(2000)
            # tcpclient.close()

            # Bind to a UDP port to talk
            # self.network_client = UDPclient(2000)
            self.network_client.update((self.udp_host, udp_port1))

            # self.network_client_ack = UDPclient(4000)
            self.network_client_ack.update((self.udp_host, udp_port2))
            self.signing = Aes(self.key)

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

    def xy_mapping(self, x, y):
        max_x = 450//self.regionSize + 1
        return (y//self.regionSize)*max_x + (x//self.regionSize)

    def send_state(self):
        ret = True
        display = FrameDisplay('{}: Sending frame'.format(self.frame_name))
        self.cam = Webcam()
        self.currentSeqNo = [1]*(self.xy_mapping(450, 600) + 1)
        self.lastAck = [1]*(self.xy_mapping(450, 600) + 1)
        self.cheating = [1]*(self.xy_mapping(450, 600) + 1)
        self.queue = [queue.Queue()
                      for i in range(0, 1 + self.xy_mapping(450, 600))]
        self.last = [np.zeros((self.regionSize, self.regionSize, 3),
                              dtype=np.uint8)
                     for i in range(0, 1+self.xy_mapping(450, 600))]

        t1 = threading.Thread(target=self.recv_ack)

        for x in range(0, 450, self.regionSize):
            for y in range(0, 600, self.regionSize):
                self.currentSeqNo[self.xy_mapping(x, y)] = 0
                self.lastAck[self.xy_mapping(x, y)] = 0

        t1.start()

        fn = 0
        self.frames_sent = 1
        self.ack_recvd = 1
        while ret:
            ret, frame = self.cam.getFrame()
            if ret:
                frame = cv2.GaussianBlur(frame, (3, 3), 0)
                ret = display.showFrame(frame)

                flag = 0
                if time.time() - self.time_last > self.time_waiting:
                    flag = 1
                    self.time_last = time.time()

                for x in range(0, 450, self.regionSize):
                    for y in range(0, 600, self.regionSize):

                        # self.cheating[self.xy_mapping(x,y)] ^= 1
                        # if self.cheating[self.xy_mapping(x,y)]:
                        #     fn += 1
                        #     continue

                        while self.queue[self.xy_mapping(x, y)].qsize() > 100:
                            self.queue[self.xy_mapping(x, y)].get()
                            self.lastAck[self.xy_mapping(x, y)] += 1

                        if (flag or
                            np.sum(np.absolute(
                                self.last[self.xy_mapping(x, y)] -
                                frame[x:min(x + self.regionSize, 450),
                                      y:min(y + self.regionSize, 600)])) >
                            (self.regionSize *
                             self.regionSize *
                             self.threshold)):

                            self.currentSeqNo[self.xy_mapping(x, y)] += 1
                            self.queue[self.xy_mapping(x, y)].put(
                                frame[x:min(x + self.regionSize, 450),
                                      y:min(y + self.regionSize, 600)])
                            frame_data = self.img_format.encode(
                                frame[x:min(x + self.regionSize, 450),
                                      y:min(y + self.regionSize, 600)])
                            packet_data = self.packetFormat.pack(
                                x, y, self.currentSeqNo[self.xy_mapping(x, y)],
                                self.signing.sign(frame_data), frame_data)

                            try:
                                self.network_client.send(packet_data)
                                self.frames_sent += 1
                            except:
                                print("network unreachable")

                            print("Current stats: ", fn, self.frames_sent,
                                  self.ack_recvd, self.threshold,
                                  self.jpeg_quality, end="\r")
                            # self.logging.log(("Sent frame ", x, " ", y,
                            # "of length", len(packet_data),
                            # self.currentSeqNo[self.xy_mapping(x, y)]))
                        else:
                            fn += 1
                            # self.logging.log(("Frame not sent ",fn, fs))

    def recv_ack(self):
        last = 0
        print("Receiving ack")
        while 1:
            data, new_addr = self.network_client_ack.recv()
            x, y, ack, sign = self.packetFormat.unpack_ack(data)
            self.recved_frames += 1

            # self.logging.log("Received ack")
            if(ack <= self.lastAck[self.xy_mapping(x, y)]):
                continue

            for i in range(0, min(ack - self.lastAck[self.xy_mapping(x, y)],
                                  self.queue[self.xy_mapping(x, y)].qsize())):
                self.queue[self.xy_mapping(x, y)].get()

            self.ack_recvd += 1
            self.last[self.xy_mapping(x, y)] = (
                self.queue[self.xy_mapping(x, y)].get())
            self.lastAck[self.xy_mapping(x, y)] = ack
            self.network_client_ack.update(new_addr)

            if time.time() - last > 2:
                last = time.time()
                if self.ack_recvd > 0.5*self.frames_sent:
                    if self.threshold > self.lower_thresh:
                        self.threshold *= 0.99
                    if self.jpeg_upper > self.jpeg_quality:
                        self.jpeg_quality *= 1.01
                else:
                    if self.threshold < self.upper_thresh:
                        self.threshold *= 1.01
                    if self.jpeg_lower < self.jpeg_quality:
                        self.jpeg_quality *= 0.99

                self.img_format.set_quality(self.jpeg_quality)

    def recv_state(self):
        matrix_img = np.zeros((480, 640, 3), dtype=np.uint8)
        display = FrameDisplay('{}: Receiving frame'.format(self.frame_name))
        ret = True
        while ret:
            data, new_addr = self.network_client.recv()
            x, y, ack, sign, frame_data = self.packetFormat.unpack(data)

            # Check validity of packet
            if self.signing.check_sign(sign, frame_data):
                # self.logging.log((x, " ", y,
                # "Got frame of length ", len(data)))
                matrix_img[x:min(x + self.regionSize, 450),
                           y:min(y + self.regionSize, 600)] = (
                               self.img_format.decode(frame_data))

                ret = display.showFrame(matrix_img)
                packet_data = self.packetFormat.pack_ack(
                                x, y, ack, sign)

                if self.network_client_ack.send(packet_data) < 1:
                    print("could not send ack")
                # Update the latest address
                # Should be handled inside recv
                self.network_client.update(new_addr)
                # self.network_client_ack.update(new_addr)

# Begin execution
if len(sys.argv) < 3:
    print("Usage: python movi.py SERVER|CLIENT host port")
    exit(1)

MoVi(sys.argv[1], sys.argv[2])
