"Create a UDP listening server"

import socket


class UDPserver:
    "Handles logic of creating and binding socket for server."

    def __init__(self, port, host="0.0.0.0"):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        print("Listening on %s:%d" % self.server_address)

        self.target_address = ("0.0.0.0", 10000)

    def get_hello(self):
        "Wait for connection from client."
        data, address = self.socket.recvfrom(4096)
        self.target_address = address
        print("Received hello from %s:%d" % address)
        print("Hello message: %s" % data)
        self.socket.sendto("Cool".encode(),
                           self.target_address)

    def talk(self):
        "Listens for messages and responds."
        while True:
            data, address = self.socket.recvfrom(4096)

            print('received %s bytes from %s' % (len(data), address))
            print(data.decode())

            if data:
                sent = self.socket.sendto(data, address)
                print('sent %s bytes back to %s' % (sent, address))

    def send(self, data):
        "Sends the provided data to target_address."
        self.socket.sendto(data, self.target_address)

    def update(self, new_addr):
        """
        To update the target address on receiving
        a valid packet from some other address.
        """
        self.target_address = new_addr
