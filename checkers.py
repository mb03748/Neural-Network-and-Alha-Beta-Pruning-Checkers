from checkersState import checkersState


class checkers:

	def __init__(self, p1, p2, startState = []):
		if not startState:
			startState = [  [ 0, -1,  0, -1,  0, -1,  0, -1],
							[-1,  0, -1,  0, -1,  0, -1,  0],
							[ 0, -1,  0, -1,  0, -1,  0, -1],
							[ 0,  0,  0,  0,  0,  0,  0,  0],
							[ 0,  0,  0,  0,  0,  0,  0,  0],
							[ 1,  0,  1,  0,  1,  0,  1,  0],
							[ 0,  1,  0,  1,  0,  1,  0,  1],
							[ 1,  0,  1,  0,  1,  0,  1,  0]    ]
		
		self.currentState = checkersState(startState)
		self.p1 = p1
		self.p2 = p2
		self.turn = 1


	def forceSetState(self, state):
		self.currentState = checkersState(state)
		self.turn = 1
	
	
	def getState(self):
		return self.currentState.state


	def singleMove(self):
		if self.currentState.hasEnded() == 0:
			if self.turn % 2 == 1:
				print("Waiting for player 1")
				self.currentState = self.p1.makeMove(self.currentState)
			else:
				print("Waiting for player 2")
				self.currentState = self.p2.makeMove(self.currentState.invert()).invert()
			self.turn += 1
			return True
		return False
		

	def singleLoop(self):
		print(self.currentState)

		while self.singleMove():
			print(self.currentState)
			
		if self.currentState.hasEnded() == 1:
			print("Victory for Player 1")
		else:
			print("Victory for Player 2")

		print(self.turn)


