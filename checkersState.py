from mxnet import ndarray as nd
import random


class checkersState:

	def __init__(self, state):
		self.state = nd.array(state).reshape(8,8).astype(int)
		self.moveMap = nd.array([[-1,-1], [-1, 1], [1, 1], [1, -1],
								 [-2,-2], [-2, 2], [2, 2], [2, -2]]).astype(int)
		self.moveChains = []

	
	def seqPositions(self, moveChain):
		lis= [moveChain[0][0].asnumpy().tolist()]
		for move in moveChain:
			pos, m_val = move
			m = self.moveMap[m_val - 1, :]
			target = m + pos
			lis.append(target.asnumpy().tolist())
		return lis
	
	
	def allSeqPositions(self):
		lis =[]
		for i in self.getActualPossMoves():
			lis.append(self.seqPositions(i))
		return lis
		

	def upperMovesOfPosition(self, pos):
		i, j = pos
		state = self.state
		upper = []
		if i - 2 >= 0 and j - 2 >= 0 and state[i - 2, j- 2] == 0 and state[i- 1, j - 1] < 0:
			upper.append([pos.copy(), 5])
		if i - 2 >= 0 and j + 2 <= 7 and state[i - 2, j + 2] == 0 and state[i - 1, j + 1] < 0:
			upper.append([pos.copy(), 6])
		if state[i, j] > 1:
			if i + 2 <= 7 and j - 2 >= 0 and state[i + 2, j - 2] == 0 and state[i + 1, j - 1] < 0:
				upper.append([pos.copy(), 8])
			if i + 2 <= 7 and j + 2 <= 7 and state[i + 2, j + 2] == 0 and state[i + 1, j + 1] < 0:
				upper.append([pos.copy(), 7])
		return upper


	def lowerMovesOfPosition(self, pos):
		i, j = pos
		state = self.state
		lower = []
		if i - 1 >= 0 and j - 1 >= 0 and state[i - 1, j - 1] == 0:
			lower.append([pos.copy(), 1])
		if i - 1 >= 0 and j + 1 <= 7 and state[i - 1, j + 1] == 0:
			lower.append([pos.copy(), 2])
		if state[i, j] > 1:
			if i + 1 <= 7 and j - 1 >= 0 and state[i + 1, j - 1] == 0:
				lower.append([pos.copy(), 4])
			if i + 1 <= 7 and j + 1 <= 7 and state[i + 1, j + 1] == 0:
				lower.append([pos.copy(), 3])
		return lower

    
	def getPossMoves(self):
		state = self.state
		lower, upper = [], []
		yetUpper = False
		pos = nd.zeros(shape = 2).astype(int)

		for i in range(state.shape[0]):
			for j in range(state.shape[1]):
				pos[:] = i,j
				if state[i, j] > 0:
					if yetUpper:
						upper.extend(self.upperMovesOfPosition(pos))
					else:
						u = self.upperMovesOfPosition(pos)
						if not u:
							lower.extend(self.lowerMovesOfPosition(pos))
						else:
							upper.extend(u)
							yetUpper = True						
		if yetUpper:
			r = upper
		else:
			r = lower
		random.shuffle(r)
		return r, yetUpper


	def applyMove(self, move):
		state = self.state.copy()
		pos, m_val = move
		m = self.moveMap[m_val - 1, :]
		target = m + pos
		state[pos[0], pos[1]], state[target[0], target[1]] = state[target[0], target[1]], state[pos[0], pos[1]]

		if m_val >= 4:
			mid = m/2 + pos
			state[mid[0], mid[1]] = 0
			
		if target[0] == 0 and abs( state[target[0], target[1]].asscalar() ) == 1:
			state[target[0], target[1]] = state[target[0], target[1]] * 3
		
		return checkersState(state)


	def hasEnded(self):
		state = self.state
		if (state < 0).sum() == 0:
			return 1
		if (state > 0).sum() == 0:
			return -1
		if len(self.getPossMoves()[0]) == 0:
			return -1
		return 0


	def invert(self):
		state = self.state.copy()
		state = state * -1
		state = state.flip(axis = 0)
		state = state.flip(axis = 1)
		return checkersState(state)


	def getActualPossMoves(self):
		if self.moveChains:
			return self.moveChains
		moves, yetUpper = self.getPossMoves()
		if not yetUpper:
			self.moveChains = [[i] for i in moves]
			return self.moveChains
		else:
			moveChains = [[i] for i in moves]
			lastStates = [checkersState(self.state) for i in moves]
			ind = 0
			while ind < len(lastStates):
				cMoveChain = moveChains[ind]
				cLastState = lastStates[ind]
				lastMove = cMoveChain[-1]
				pos, m_val = lastMove
				m = self.moveMap[m_val - 1, :]
				new_pos = m + pos
				new_state = self.applyMove(lastMove)
				new_moves = self.upperMovesOfPosition(new_pos)
				if not new_moves:
					ind += 1
				else:
					one_new_move = new_moves.pop()
					for i in new_moves:
						moveChains.append(cMoveChain + [i])
						lastStates.append(checkersState(new_state.state))
					moveChains[ind].append(one_new_move)
					lastStates[ind] = new_state
			self.moveChains = moveChains
			return self.moveChains
			

	def applyMoveChain(self, moveChain):
		state = self
		for i in moveChain:
			state = state.applyMove(i)
		return state


	def __str__(self):
		return self.state.__str__()
		
		
	def __hash__(self):
		return int("".join(map(str, (self.state + 3).reshape(-1).asnumpy().tolist())))


	def __eq__(self, other):
		return self.__hash__() == other.__hash__()





