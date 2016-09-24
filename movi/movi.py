# -*- coding: utf-8 -*-
"Contains initialization code"

from network.udpserver import UDPserver
from network.udpclient import UDPclient
import sys


class MoVi:
    "Begin of moVi"

    def __init__(self, mode, port, host):

        if mode == "SERVER":
            server = UDPserver(port, host)
            server.talk()
        elif mode == "CLIENT":
            client = UDPclient(port, host)
            client.talk()
        else:
            print("Wrong mode")
            exit(1)

if len(sys.argv) < 4:
    print("Usage: python movi.py SERVER|CLIENT host port")
    exit(1)

MoVi(sys.argv[1], int(sys.argv[3]), sys.argv[2])
