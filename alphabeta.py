def AlphaBeta(state, depth, heuristic):
    return minimax(state, depth, float('-inf'), float('inf'), True, depth, heuristic)


def minimax(state, depth, alpha, beta, maximizingPlayer, max_depth, heuristic): #position is the starting point, depth is of tree, mP is a boolean

    if depth == 0 or state.hasEnded() != 0:
        a = heuristic(state, maximizingPlayer, max_depth - depth)
        return a

    if maximizingPlayer:
        for i in state.getActualPossMoves():
            num = minimax(state.applyMoveChain(i).invert(), depth-1, alpha, beta, False, max_depth, heuristic)
            if num > alpha:
                alpha = num
                if max_depth == depth:
                    arg = i    
            if beta <= alpha:
                break
        if max_depth == depth:
            return arg
        return alpha

    else:
        for i in state.getActualPossMoves():
            num = minimax(state.applyMoveChain(i).invert(), depth-1, alpha, beta, True, max_depth, heuristic)
            beta = min(beta,num)
            if beta <= alpha:
                break
        return beta

     
