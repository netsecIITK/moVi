"Create a UDP client"

import socket


class UDPclient:
    "Handles client logic using UDP."

    def __init__(self, port, host="0.0.0.0"):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def talk(self):
        "Sends a message to the server, receives, and exits."
        message = "mymessage".encode()
        try:
            # Send data
            print('sending "%s"' % message)
            sent = self.socket.sendto(message, self.server_address)
            print("Sent %d" % sent)

            # Receive response
            data, _ = self.socket.recvfrom(4096)
            print('received "%s"' % data)

        finally:
            print("Closing")
            self.socket.close()

    def send_hello(self):
        "Sends a hello to the server."
        message = "Hello server!".encode()
        self.socket.sendto(message, self.server_address)
        data, _ = self.socket.recvfrom(4096)
        print("Received %s" % data)

    def recv(self):
        "Receives a datagram (can be valid or invalid)."
        return self.socket.recvfrom(4096)

    def update(self, new_addr):
        "Update the server_address on receiving a valid packet."
        self.server_address = new_addr
