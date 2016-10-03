"""
Takes a frame, its location, and more info.
Puts that into a bytestream.
"""

import pickle


class MoViPack:
    "Handles the logic of assembling information into packets"

    def __init__(self):
        print("Pickler")

    def get_pickles(self, frame):
        k = 10
        return [pickle.dumps(frame[x:(x+k), y:(y+k)])
                for x in range(0, 480, k) for y in range(0, 640, k)]

    def dummy(self, string):
        return pickle.dumps(string)
