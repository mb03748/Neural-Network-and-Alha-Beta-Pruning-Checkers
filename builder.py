from checkers import checkers
from computerPlayer import computerPlayer
from checkersState import checkersState
import pandas as pd


class DataBuilder(checkers):
	
	def __init__(self, startState = []):
		super(DataBuilder, self).__init__(computerPlayer(3), computerPlayer(3), startState)
		self.states = dict()
		self.initState = self.currentState.state.copy().asnumpy().tolist()

	
	def read_csv(self):
		try:
			df = pd.read_csv('data.csv', header = 0)
		except:
			print("Previous file not found, continuing anyway")
			return
		for i in range(len(df)):
			state = df.iloc[i, :-2].tolist()
			cstate = checkersState(state)
			lis = df.iloc[i, -2:].tolist()
			self.states[cstate] = lis


	def writeCsv(self):
		print("Writing, Be careful")
		lis = []
		for i in self.states:
			l = i.state.reshape(-1).asnumpy().tolist() + self.states[i]
			lis.append(l)
		df = pd.DataFrame(lis)
		df.to_csv('data.csv', index = False)
		print("Done writing")


	def makeIter(self, n):
		
		total_turns = 0
		for i in range(n):
			print("ITER NUMBER --------------------- ", i + 1)
			currentStates = dict()
			self.forceSetState(self.initState)
			if self.currentState not in currentStates:
				currentStates[self.currentState] = [0, 1]
			else:
				currentStates[self.currentState][1] += 1
			while self.singleMove():
				if self.currentState not in currentStates:
					currentStates[self.currentState] = [0, 1]
				else:
					currentStates[self.currentState][1] += 1
				if self.turn % 10 == 0:
					print('checkPoint')
			if self.currentState.hasEnded() == 1:
				for j in currentStates:
					currentStates[j][0] = currentStates[j][1]
			for j in currentStates:
				if j not in self.states:
					self.states[j] = currentStates[j]
				else:
					self.states[j][0] += currentStates[j][0]
					self.states[j][1] += currentStates[j][1]
			total_turns += self.turn
			self.writeCsv()
		print(total_turns)
		print(len(self.states))
				

	def makeIterAndSave(self, n):
		self.makeIter(n)


	def buildMoreData(self, n):
		self.read_csv()
		self.makeIterAndSave(n)

