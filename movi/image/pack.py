"""
Takes a frame, and returns the pickles of
the updated regions in the frame
"""

import pickle


class MoViPack:
    "Handles the logic of packing and region division"

    def __init__(self):
        print ("Pickler")

    def get_pickles(self, frame):
        return pickle.dumps(frame)
