"Create a UDP client"

import socket


class UDPclient:
    "Handles client logic using UDP."

    def __init__(self, port, host="0.0.0.0"):
        "Bind to the supplied port"
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((host, port))
        print("UDP Listening on %s:%d" % self.address)

    def send(self, data):
        "Sends the provided data to target_address."
        return self.socket.sendto(data, self.target_address)

    def recv(self):
        "Receives a datagram (can be valid or invalid)."
        # TODO Shift to recvfrom_into
        # Into: To use a common buffer, avoid making extra bytestrings
        return self.socket.recvfrom(4096)

    def update(self, new_addr):
        "Update the server_address on receiving a valid packet."
        # TODO Remove after above is modified
        self.target_address = new_addr
