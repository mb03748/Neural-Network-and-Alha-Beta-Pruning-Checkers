def heuristic(state, maximizingPlayer, depth):
    return (((state.state > 0).sum() - (state.state < 0).sum()).asscalar())  * [-1, 1][maximizingPlayer] * 1000 - (depth)
	
