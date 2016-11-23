# -*- coding: utf-8 -*-
"Contains the code for the broker for UDP Hole Punching"

import threading

from network.udpclient import UDPclient
from network.tcpserver import TCPserver
from network.tcpclient import TCPclient

hostname = '0.0.0.0'
tcp_port = 8500
udp_frame_port = 3500
udp_ack_port = 4500

class Broker:
    "Begin Broker"

    def __init__(self):
        self.tcp_broker = TCPserver(tcp_port, hostname)
        self.udp_frame_broker = UDPclient(udp_frame_port)
        self.udp_ack_broker = UDPclient(udp_ack_port)

        self.state_tcp = False
        self.state_udp1 = False
        self.state_udp2 = False

        self.sender_socket = None
        self.stcp_save = ('', 0)
        self.supd1_save = ('', 0)
        self.sudp2_save = ('', 0)

        self.recv_socket = None
        self.ctcp_save = ('', 0)
        self.cupd1_save = ('', 0)
        self.cudp2_save = ('', 0)

        self.recv_cl = 0   # Count of receiver connections

        self.runner()

    # Connection listener initiator
    def runner(self):
        t = [threading.Thread(target=self.tcp_listener),
                threading.Thread(target=self.udp1_listener),
                threading.Thread(target=self.udp2_listener)]

        for rt in list(map(lambda x: x.start(), t)):
            rt.join()

    # When both have connected
    def exchange_info(self):
        self.recv_cl = 0
        self.state_tcp = False
        self.state_udp1 = False
        self.state_udp2 = False

        # Send to SERVER first
        self.sender_socket.send(
                str("{} {} {} {}".format(
                    self.ctcp_save[0],
                    self.ctcv_save[1],
                    self.cudp1_save[1],
                    self.cudp2_save[1])))
        self.sender_socket.close()

        # Send server's info to client now
        self.recv_socket.send(
                str("{} {} {} {}".format(
                    self.stcp_save[0],
                    self.stcv_save[1],
                    self.sudp1_save[1],
                    self.sudp2_save[1])))
        self.recv_socket.close()

    def udp1_listener(self):
        while True:
            data, cl_addr = self.udp_frame_broker.recv()
            print("Received UDP1 from", cl_addr)
            if self.state_udp1 == False:
                self.sudp1_save = cl_addr
                self.state_udp1 = True
            else:
                self.recv_cl += 1
                self.cudp1_save = cl_addr

                if self.recv_cl == 3:
                    self.exchange_info()

    def udp2_listener(self):
        while True:
            data, cl_addr = self.udp_ack_broker.recv()
            print("Received UDP2 from", cl_addr)
            if self.state_udp2 == False:
                self.sudp2_save = cl_addr
                self.state_udp2 = True
            else:
                self.recv_cl += 1
                self.cudp2_save = cl_addr

                if self.recv_cl == 3:
                    self.exchange_info()

    def tcp_listener(self):
        for (cl_socket, cl_addr) in self.tcp_broker.connection_generator():
            print("Received TCP from", cl_addr)
            if self.state_tcp == False:
                self.stcp_save = cl_addr
                self.sender_socket = cl_socket
                self.state_tcp = True
            else:
                self.recv_cl += 1
                self.ctcp_save = cl_addr
                self.recv_socket = cl_socket

                if self.recv_cl == 3:
                    self.exchange_info()
