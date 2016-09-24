"Create a UDP listening server"

import socket


class UDPserver:
    "Handles logic of creating and binding socket for server."

    def __init__(self, port, host="0.0.0.0"):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        print("Listening on %s:%d" % self.server_address)

    def talk(self):
        "Listens for messages and responds."
        while True:
            data, address = self.socket.recvfrom(4096)

            print('received %s bytes from %s' % (len(data), address))
            print(data.decode())

            if data:
                sent = self.socket.sendto(data, address)
                print('sent %s bytes back to %s' % (sent, address))
