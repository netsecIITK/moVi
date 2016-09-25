"""
Unpacks the list of pickles, and returns new frame
"""

import pickle


class MoViUnpack:
    "Handles the logic of unpacking and reconstruction"

    def __init__(self):
        print ("Unpickler")

    def get_frame(self, frame_data):
        return pickle.loads(frame_data)
