""" Type of packet, Diff or Ack"""

from enum import Enum

class PacketType(Enum):
	diff = 0x0
	ack  = 0x1