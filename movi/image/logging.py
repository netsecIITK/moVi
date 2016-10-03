"""
Log the events into the log directory as a different thread
"""

from multiprocessing import Pool

class Logging:

    def __init__(self):
        self.pool = Pool(processes=1)

    def log(self, string):
        self.pool.apply_async(print, [string])
