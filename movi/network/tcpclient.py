"""
A basic TCP client to negotiate the connection
details initially.
It is closed down as soon as the UDP connection is
up and running.
"""

import socket


class TCPclient:
    "Handles logic of creating socket and talking to server socket."

    def __init__(self, port, host):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("TCP talking to %s:%d" % self.server_address)
        self.socket.connect(self.server_address)

    def get_information(self, my_udp_port):
        """
        Communicates with server. Exchanges secret key
        and UDP port numbers to use
        """
        key = self.socket.recv(20).decode()
        self.socket.send(str(my_udp_port).encode())
        udp_port = int(self.socket.recv(10))
        self.socket.close()

        return (key, udp_port)

    def close(self):
        print("Closing TCP socket to address {}:{}"
              .format(*self.server_address))
        self.socket.close()
