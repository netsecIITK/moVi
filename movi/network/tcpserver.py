"""
A basic TCP server to negotiate the connection
details initially.
It is closed down as soon as the UDP connection is
up and running.
"""

import socket


class TCPserver:
    "Handles logic of creating and binding socket for server."

    def __init__(self, port, host="0.0.0.0"):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        print("TCP Listening on %s:%d" % self.server_address)

    def connection_information(self, my_udp_port):
        """
        Given a UDP port, waits for connections, and gets information
        from any new connection. Communicates an encryption key,
        and exchange UDP port number
        """
        for (client_socket, client_addr) in self.connection_generator():
            self.target_address = client_addr
            # target_address contains hostname of target
            # get_information will provide it's UDP port
            yield (self.target_address[0],
                   self.get_information(client_socket, my_udp_port))

    def connection_generator(self):
        """
        Simply provides a connection's socket and address as a generator.
        """
        yield self.socket.accept()

    def get_information(self, client_socket, my_udp_port):
        """
        Communicates with a connected client. Exchanges secret key
        and UDP port numbers to use
        """
        key = "abcd"
        client_socket.send(key.encode())
        udp_port = int(client_socket.recv(10).decode())
        client_socket.send(str(my_udp_port).encode())
        client_socket.close()

        return (key, udp_port)

    def close(self):
        print("Closing TCP socket on address {}:{}"
              .format(*self.server_address))
        self.socket.close()
