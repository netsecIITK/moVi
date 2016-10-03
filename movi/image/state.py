""" Maintains current state and also the last acked state """

from queue import Queue
import numpy as np

class State:
	
	"""initiallize the current state map and per region queue"""
	def __init__(self, regionSize):
		self.currentState = dict()
		self.regionQueues = dict()
		self.lastAckedRegions = dict()
		self.lastAckedStates = dict()

		for x in range(0, 450, regionSize):
			for y in range(0, 600, regionSize):
				self.currentState[(x,y)] = 0
				self.regionQueues[(x,y)] = Queue()
				self.lastAckedRegions[(x,y)] = np.zeros((480, 640, 3), dtype=np.uint8)
				self.lastAckedStates[(x,y)] = 0

		self.maximumStateNumber = 2**32 - 1

	def incrementCurrentState(self,x,y):
		self.currentState[(x,y)] += 1
		self.currentState[(x,y)] %= self.maximumStateNumber

	def currentState(self,x,y):
		return self.currentState[(x,y)]

	"""buffer the frame"""
	def addFrame(self, x, y, frame):
		self.regionQueues[(x,y)].put(frame)

	""" Updates the base frame for a region whenever an ack is received 
		and dequeues the frames in between""" 
	def ackReceived(self, x, y, receivedState):
		
		if receivedState > self.lastAckedStates[(x,y)]:	
			temp = receivedState - self.lastAckedStates[(x,y)]
			self.lastAckedStates[(x,y)] = receivedState

			for i in range(0,temp):
				if i == temp -1:
					self.lastAckedRegions[(x,y)] = self.regionQueues[(x,y)].get()
				else
					self.regionQueues[(x,y)].get()

	"""returns the relative difference between two frames """
	def diff(self, x, y, frame):
		return np.absolute(self.currentState[(x,y)] - 
			frame)/np.linalg.norm(self.currentState[(x,y)], 1)

