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
        return struct.pack("<I", integer)

    def _int_decode(self, int_bytes):
        return struct.unpack("<I", int_bytes)[0]

    def pack(self, x, y, seq_no, signature, frame):
        self.bytea = bytearray()
        self.bytea += (self._int_encode(x) + self._int_encode(y) 
            + self._int_encode(seq_no))
        self.bytea.extend(signature[0:4])
        self.bytea.extend(frame)
        return self.bytea

    def unpack(self, data):
        return (self._int_decode(data[0:4]),
                self._int_decode(data[4:8]),
                self._int_decode(data[8:12]),
                data[12:16],
                np.fromstring(data[16:], np.uint8))
    
    def pack_ack(self, x, y, seq_no, signature):
        self.bytea = bytearray()
        self.bytea += (self._int_encode(x) + self._int_encode(y) 
            + self._int_encode(seq_no))
        self.bytea.extend(signature[0:4])
        return self.bytea

    def unpack_ack(self, data):
        return (self._int_decode(data[0:4]),
                self._int_decode(data[4:8]),
                self._int_decode(data[8:12]),
                data[12:16])
