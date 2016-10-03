"""
Takes a frame, its location, and more info.
Puts that into a bytestream.
"""

import numpy as np
import struct


class PacketFormat:
    "Handles the logic of assembling information into packets"

    def __init__(self):
        self.bytea = bytearray()

    def _int_encode(self, integer):
        return struct.pack("<H", integer)

    def _int_decode(self, int_bytes):
        return struct.unpack("<H", int_bytes)[0]

    def pack(self, x, y, signature, frame):
        self.bytea = bytearray()
        self.bytea += self._int_encode(x) + self._int_encode(y)
        self.bytea.extend(signature[0:4])
        self.bytea.extend(frame)
        return self.bytea

    def unpack(self, data):
        return (self._int_decode(data[0:2]),
                self._int_decode(data[2:4]),
                data[4:8],
                np.fromstring(data[8:], np.uint8))
