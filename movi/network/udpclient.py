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
